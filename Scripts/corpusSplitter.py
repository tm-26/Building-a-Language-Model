import json
import os
import random
from datetime import datetime


def prepend(myList, string):
    string += '{0}'
    myList = [string.format(word) for word in myList]
    return myList


def splitCorpus():
    startTime = datetime.now()

    # Variable Declaration
    corpusSet = []

    # Getting all folders of corpus
    folders = os.listdir("../British National Corpus, Baby edition/Texts")
    for folderName in folders:
        corpusSet.extend(
            prepend(os.listdir("../British National Corpus, Baby edition/Texts/" + folderName), folderName + "/"))

    percentageOfTrainingData = 0.75
    random.shuffle(corpusSet)
    splitPoint = round(len(corpusSet) * percentageOfTrainingData)
    trainingSet = corpusSet[:splitPoint]
    testingSet = corpusSet[splitPoint:]

    with open("../Data/trainingSet.json", "w+") as file:
        json.dump(trainingSet, file)
    print("Created training set in ../Data/trainingSet.json")
    with open("../Data/testingSet.json", "w+") as file:
        json.dump(testingSet, file)
    print("Created testing set in ../Data/testingSet.json")

    print("Training and testing built in ", datetime.now() - startTime)


if __name__ == "__main__":
    splitCorpus()
