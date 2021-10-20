import json
import os
import random
import sys
from calculateSentenceProbability import linearInterpolation
from lexiconBuilder import createLexicon
from languageModelBuilder import getSmallerModel


def continueSentence(currentSentence, flavour):
    # Variable Declaration
    possibleSentences = {}
    unigram = {}

    if flavour != "vanilla":
        getSmallerModel(1)
        unigram = json.load(open("../Data/vanilla 1-gram count.json", "r", encoding="utf16"))

    if not os.path.exists("../Data/lexicon.json"):
        print("lexicon.json not found, generating one now...")
        createLexicon()
    lexicon = json.load(open("../Data/lexicon.json", "r", encoding="utf16"))
    lexicon["</s>"] = 0

    arrayOfModels = []
    for i in range(1, 4):
        getSmallerModel(i, flavour)
        arrayOfModels.append(
            json.load(open("../Data/" + flavour + " " + str(i) + "-gram model.json", "r", encoding="utf16")))

    while True:
        words = currentSentence.split()[-2:]
        currentSentence = currentSentence + " "
        for word in lexicon.keys():
            if word == ' ' or word == '' or word is None:
                continue
            words.append(word)
            possibleSentences[currentSentence + word] = float(
                linearInterpolation(flavour, ' '.join(words), arrayOfModels, unigram, False, False))
            del words[-1]
        currentSentence = random.choices(list(possibleSentences.keys()), list(possibleSentences.values()))[-1]
        possibleSentences = {}
        myWords = currentSentence.split()
        if myWords[-1] == "</s>" or len(myWords) >= 100:
            print(currentSentence[:-4])
            break
        else:
            print(currentSentence)


if __name__ == "__main__":
    continueSentence(sys.argv[1], sys.argv[2])
