import json
import os
import sys

from corpusSplitter import splitCorpus
from datetime import datetime
from lexiconBuilder import createLexicon
from nltk.corpus.reader.bnc import BNCCorpusReader

# Global Variable Declaration
count = 0


def getSmallerModel(N, flavour="vanilla"):
    if flavour == "laplace":
        if not os.path.exists("../Data/laplace " + str(N) + "-gram model.json"):
            print("laplace " + str(N) + "-gram model not found, generating one now")
            buildModel(N, flavour)
    elif not os.path.exists("../Data/" + flavour + " " + str(N) + "-gram count.json"):
        print(flavour + str(N) + "-gram count not found, generating one now")
        buildModel(N, flavour)


def createCount(words, N, model):
    global count
    for i in range(len(words) - (N - 1)):
        word = ""
        for j in range(N):
            if word != ' ':
                word += words[i + j].replace(" ", "")
                if j + 1 != N:
                    word += " "
        if len(word.split()) == N:
            if word in model:
                model[word] = model.get(word) + 1
            else:
                model.update({word: 1})
            count += 1
    return model


def buildModel(N, smoothingType=None):
    startTime = datetime.now()
    if N <= 0:
        print("An error occurred: N smaller then 1")
        exit(-1)
    if smoothingType is None or smoothingType == '0' or smoothingType.lower() == "none" or smoothingType.lower() == "vanilla" or smoothingType.lower() == 'v':
        # Variable Deceleration
        corpus = BNCCorpusReader(root="../British National Corpus, Baby edition/Texts", fileids=r'[A-K]/\w*/\w*\.xml')
        model = {}
        global count
        count = 0
        progress = 0

        if not (os.path.exists("../Data/trainingSet.json")):
            splitCorpus()
        trainingSet = json.load(open("../Data/trainingSet.json", "r"))

        for file in trainingSet:
            sentences = corpus.sents(file)
            for sentence in sentences:
                sentence.insert(0, "<s>")
                sentence.append("</s>")
                model = createCount(sentence, N, model)
            progress += 1
            print(str(progress) + "/" + str(len(trainingSet)))
        with(open("../Data/vanilla " + str(N) + "-gram count.json", "w+", encoding="utf16")) as file:
            json.dump(model, file, ensure_ascii=False)

        print("Vanilla language count successfully built in ../Data/vanilla " + str(N) + "-gram count.json")

        if N == 1:
            model = {i: (j / count) for i, j in model.items()}
        else:
            getSmallerModel(N - 1)
            smallerModel = json.load(open("../Data/vanilla " + str(N - 1) + "-gram count.json", "r", encoding="utf16"))
            model = {i: (j / smallerModel.get(i.rsplit(' ', 1)[0])) for i, j in model.items()}
        with(open("../Data/vanilla " + str(N) + "-gram model.json", "w+", encoding="utf16")) as file:
            json.dump(model, file, ensure_ascii=False)

        print("Vanilla language model successfully built in ../Data/vanilla " + str(N) + "-gram model.json")
        print("Model built in ", datetime.now() - startTime)

    else:
        getSmallerModel(N)
        model = json.load(open("../Data/vanilla " + str(N) + "-gram count.json", "r", encoding="utf16"))

        if smoothingType == '1' or smoothingType.lower() == 'l' or smoothingType.lower() == "laplace":
            print("vanilla " + str(N) + "-gram count found, generating laplace model...")

            # Variable Deceleration
            if not os.path.exists("../Data/lexicon.json"):
                print("lexicon.json not found, generating one now...")
                createLexicon()
            lexicon = json.load(open("../Data/lexicon.json", "r", encoding="utf16"))
            total = sum(model.values()) + len(lexicon)
            modelCount = {}

            if N == 1:
                for i, j in model.items():
                    modelCount[i] = j + 1
                    model[i] = (j + 1) / total
                model["<UNK>"] = 1 / total
            else:
                getSmallerModel(N - 1)
                smallerModel = json.load(
                    open("../Data/vanilla " + str(N - 1) + "-gram count.json", "r", encoding="utf16"))
                V = len(lexicon)
                for i, j in model.items():
                    modelCount[i] = j + 1
                    model[i] = (j + 1) / (smallerModel.get(i.rsplit(' ', 1)[0]) + V)

                for word in smallerModel.keys():
                    if smallerModel.get(word) is None:
                        model[word + " <K>"] = 1 / len(smallerModel)
                    else:
                        model[word + " <K>"] = 1 / (smallerModel.get(word) + len(smallerModel))

            with(open("../Data/laplace " + str(N) + "-gram count.json", "w+", encoding="utf16")) as file:
                json.dump(modelCount, file, ensure_ascii=False)

            print("Laplace language count successfully built in ../Data/laplace " + str(N) + "-gram model.json")

            with(open("../Data/laplace " + str(N) + "-gram model.json", "w+", encoding="utf16")) as file:
                json.dump(model, file, ensure_ascii=False)

            print("Laplace language model successfully built in ../Data/laplace " + str(N) + "-gram model.json")
            print("Model built in ", datetime.now() - startTime)

        elif smoothingType == '2' or smoothingType.lower() == 'u' or smoothingType.lower() == "unk":
            print("vanilla " + str(N) + "-gram count found, generating unk model...")

            # Variable Declaration
            UNKSize = 0
            total = sum(model.values())
            modelCount = model.copy()

            if N == 1:
                for word, count in list(model.items()):
                    if count == 1:
                        del model[word]
                        del modelCount[word]
                        UNKSize += 1
                    else:
                        model[word] = count / total
                model["<UNK>"] = UNKSize / total
                modelCount["<UNK>"] = UNKSize
            else:
                getSmallerModel(N - 1, "UNK")
                smallerModel = json.load(open("../Data/UNK " + str(N - 1) + "-gram count.json", "r", encoding="utf16"))
                getSmallerModel(1)
                unigramModel = json.load(open("../Data/vanilla 1-gram count.json", "r", encoding="utf16"))

                delete = False
                for words, count in list(model.items()):
                    listOfWords = words.split()
                    for i in range(len(listOfWords)):
                        if unigramModel.get(listOfWords[i]) == 1:
                            delete = True
                            listOfWords[i] = "<UNK>"
                    if delete:
                        del model[words]
                        del modelCount[words]
                        delete = False
                    words = " ".join(listOfWords)
                    model[words] = count / smallerModel.get(words.rsplit(' ', 1)[0])
                    modelCount[words] = count

            with(open("../Data/UNK " + str(N) + "-gram count.json", "w+", encoding="utf16")) as file:
                json.dump(modelCount, file, ensure_ascii=False)

            print("UNK language count successfully built in ../Data/UNK " + str(N) + "-gram count.json")

            with(open("../Data/UNK " + str(N) + "-gram model.json", "w+", encoding="utf16")) as file:
                json.dump(model, file, ensure_ascii=False)

            print("UNK language model successfully built in ../Data/UNK " + str(N) + "-gram model.json")
            print("Model built in ", datetime.now() - startTime)

if __name__ == "__main__":
    buildModel(int(sys.argv[1]), sys.argv[2])
