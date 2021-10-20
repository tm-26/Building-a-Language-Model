import json
import languageModelBuilder
import sys
from decimal import Decimal, getcontext


def getArrayOfModels(flavour):
    arrayOfModels = []
    for i in range(1, 4):
        languageModelBuilder.getSmallerModel(i, flavour)
        arrayOfModels.append(
            json.load(open("../Data/" + flavour + " " + str(i) + "-gram model.json", "r", encoding="utf16")))
    return arrayOfModels


def main(myInput, myFlavour):
    myArrayOfModels = getArrayOfModels(myFlavour)

    unigram = {}
    if myFlavour != "vanilla":
        languageModelBuilder.getSmallerModel(1)
        unigram = json.load(open("../Data/vanilla 1-gram count.json", "r", encoding="utf16"))

    myP = linearInterpolation(myFlavour, myInput, myArrayOfModels, unigram)
    print("P(" + myInput + ") = " + str(myP))


def multiply(numbers):
    total = 1
    for myI in numbers:
        total *= myI
    return total


def handleUnknownStringForLaplace(W, model, V):
    myListOfWords = W.split()
    myListOfWords.pop()
    myListOfWords.append("<K>")
    string = ' '.join(myListOfWords)
    value = model.get(string)
    if value is not None:
        return value
    else:
        return 1 / V


def handleUnknownStringForUNK(W, model, unigramModel):
    myListOfWords = W.split()
    for myI in range(len(myListOfWords)):
        if unigramModel.get(myListOfWords[myI]) == 1 or myListOfWords[myI] not in unigramModel.keys():
            myListOfWords[myI] = "<UNK>"
    W = ' '.join(myListOfWords)
    if W in model.keys():
        return model.get(W)
    else:
        return 0


def linearInterpolation(flavour, string, arrayOfModels, unigramModel, appendSentenceToken=True, showOutput=False):
    # Variable Declaration
    P1 = []  # Unigram probability
    P2 = []  # Bigram probability
    P3 = []  # Trigram probability
    W2 = ""
    W3 = ""
    weights = [Decimal(0.1), Decimal(0.3), Decimal(0.6)]
    count = 0
    getcontext().prec = 1000
    if appendSentenceToken:
        string = "<s> " + string + " </s>"

    listOfWords = string.split()
    for word in listOfWords:
        if 0 not in P1 and count != 0 and count != (len(listOfWords) - 1):
            value = arrayOfModels[0].get(word)
            if value is not None:
                P1.append(Decimal(value))
            elif flavour == "vanilla":
                P1.append(Decimal(0))
            else:
                P1.append(Decimal(arrayOfModels[0].get("<UNK>")))

        if 0 not in P2:
            if len(W2.split()) == 2:
                # Remove first word
                W2 = W2.split(' ', 1)[1]

            if W2 == "":
                W2 += word
            else:
                W2 += " " + word

            if len(W2.split()) == 2:
                value = arrayOfModels[1].get(W2)
                if value is not None:
                    P2.append(Decimal(value))
                elif flavour == "vanilla":
                    P2.append(Decimal(0))
                elif flavour == "laplace":
                    P2.append(Decimal(handleUnknownStringForLaplace(W2, arrayOfModels[1], len(unigramModel))))
                else:
                    P2.append(Decimal(handleUnknownStringForUNK(W2, arrayOfModels[1], unigramModel)))

        if 0 not in P3:
            if len(W3.split()) == 3:
                # Remove first word
                W3 = W3.split(' ', 1)[1]

            if W3 == "":
                W3 += word
            else:
                W3 += " " + word

            if len(W3.split()) == 3:
                value = arrayOfModels[2].get(W3)
                if value is not None:
                    P3.append(Decimal(value))
                elif flavour == "vanilla":
                    P3.append(Decimal(0))
                elif flavour == "laplace":
                    P3.append(Decimal(handleUnknownStringForLaplace(W3, arrayOfModels[2], len(unigramModel))))
                else:
                    P3.append(Decimal(handleUnknownStringForUNK(W3, arrayOfModels[2], unigramModel)))
        count += 1

    if showOutput:
        print("Unigram value = ", P1, "Which when multiplied we get: ", multiply(P1))
        print("Bigram value = ", P2, "Which when multiplied we get: ", multiply(P2))
        print("Trigram value = ", P3, "Which when multiplied we get: ", multiply(P3))

    return (weights[0] * multiply(P3)) + (weights[1] * multiply(P2)) + (weights[2] * multiply(P1))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
