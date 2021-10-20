import json
import os
from datetime import datetime
from nltk.corpus.reader.bnc import BNCCorpusReader


def createLexicon():
    startTime = datetime.now()

    # Variable Declaration
    dictOfWords = {}
    uniqueCount = 0
    count = 1

    # Loading corpus
    corpus = BNCCorpusReader(root="../British National Corpus, Baby edition/Texts", fileids=r'[A-K]/\w*/\w*\.xml')
    # Getting all folders of corpus
    folders = os.listdir("../British National Corpus, Baby edition/Texts")

    for folderName in folders:
        folder = os.listdir("../British National Corpus, Baby edition/Texts/" + folderName)
        for file in folder:
            words = corpus.words("./" + folderName + "/" + file)

            for word in words:
                if word not in dictOfWords:
                    dictOfWords[word.replace(" ", "")] = uniqueCount
                    uniqueCount += 1
            print(str(count) + " / " + "182")
            count += 1
    with open("../Data/lexicon.json", "w+", encoding="utf16") as file:
        json.dump(dictOfWords, file, ensure_ascii=False)

    print("Lexicon successfully built in ../Data/lexicon.json")

    file = open("../Data/lexicon.txt", "w+", encoding='utf16')

    file.write(
        "This is a lexicon for the British National Corpus, Baby edition corpus.\nThe corpus can be located: htt"
        "ps://ota.bodleian.ox.ac.uk/repository/xmlui/handle/20.500.12024/2553\n")

    for word in dictOfWords.keys():
        file.write(word + "\n")
    print("Lexicon built in ", datetime.now() - startTime)


if __name__ == "__main__":
    createLexicon()
