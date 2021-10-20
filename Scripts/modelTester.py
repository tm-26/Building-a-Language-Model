import json
import languageModelBuilder
import os
import sys
from calculateSentenceProbability import linearInterpolation, getArrayOfModels
from datetime import datetime
from corpusSplitter import splitCorpus
from nltk.corpus.reader.bnc import BNCCorpusReader


def testModels(flavour):
    startTime = datetime.now()

    # Variable Deceleration
    corpus = BNCCorpusReader(root="../British National Corpus, Baby edition/Texts", fileids=r'[A-K]/\w*/\w*\.xml')
    unigram = {}
    arrayOfModels = getArrayOfModels(flavour)
    zeroCount = 0
    count = 0
    fileCount = 0

    if not (os.path.exists("../Data/testingSet.json")):
        splitCorpus()
    testSet = json.load(open("../Data/testingSet.json", "r"))

    if flavour != "vanilla":
        languageModelBuilder.getSmallerModel(1)
        unigram = json.load(open("../Data/vanilla 1-gram count.json", "r", encoding="utf16"))

    for file in testSet:
        sentences = corpus.sents(file)
        for sentence in sentences:
            if linearInterpolation(flavour, ' '.join(sentence), arrayOfModels, unigram) == 0:
                zeroCount += 1
            count += 1
        fileCount += 1
        print(str(fileCount) + " / " + str(len(testSet)))
    if flavour == "unk":
        print("0 probability count of the UNK models: " + str(zeroCount) + " / " + str(count))
    else:
        print("0 probability count of the " + flavour + " models: " + str(zeroCount) + " / " + str(count))
    print("Hence, the models predicted " + str(round((1 - (zeroCount / count)) * 100)) + "% of the sentences")
    print("Models tested in ", datetime.now() - startTime)


if __name__ == "__main__":
    testModels(sys.argv[1])
