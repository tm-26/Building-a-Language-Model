from calculateSentenceProbability import main
from continueMySentence import continueSentence
from corpusSplitter import splitCorpus
from languageModelBuilder import buildModel
from lexiconBuilder import createLexicon
from modelTester import testModels

if __name__ == "__main__":
    while True:
        print("Choose an operation")
        print("1) Build Lexicon")
        print("2) Create training and test set")
        print("3) Build a model")
        print("4) Calculate the probability of a sentence")
        print("5) Finish a sentence")
        print("6) Test models")
        print("7) Autofill Data folder")
        print("0) Exit")
        choice = str(input())
        choice = choice.replace(" ", "").lower()
        if choice == '1' or choice == "buildlexicon":
            createLexicon()
        elif choice == '2' or choice == "createtrainingandtestset":
            splitCorpus()
        elif choice == '3' or choice == "buildamodel":
            N = 0
            while True:
                print("Choose a flavour:")
                print("1) Unigram")
                print("2) Bigram")
                print("3) Trigram")
                print("0) Return to main menu")
                choice = str(input())
                choice = choice.replace(" ", "").lower()
                if choice == '1' or choice == "unigram":
                    N = 1
                    break
                elif choice == '2' or choice == "bigram":
                    N = 2
                    break
                elif choice == '3' or choice == "trigram":
                    N = 3
                    break
                elif choice == '0' or choice == "returntomainmenu":
                    break
                else:
                    print("Please enter a valid input")
            while True:
                print("Choose a flavour:")
                print("1) Vanilla")
                print("2) Laplace")
                print("3) UNK")
                print("0) Return to main menu")
                choice = str(input())
                choice = choice.replace(" ", "").lower()
                if choice == '1' or choice == "vanilla":
                    buildModel(N, "vanilla")
                    break
                elif choice == '2' or choice == "laplace":
                    buildModel(N, "laplace")
                    break
                elif choice == '3' or choice == "unk":
                    buildModel(N, "unk")
                    break
                elif choice == '0' or choice == "returntomainmenu":
                    break
                else:
                    print("Please enter a valid input")
        elif choice == '4' or choice == "calculatetheprobabilityofasentence":
            print("Enter your sentence ")
            sentence = input()
            while True:
                print("Choose a flavour:")
                print("1) Vanilla")
                print("2) Laplace")
                print("3) UNK")
                print("0) Return to main menu")
                choice = str(input())
                choice = choice.replace(" ", "").lower()
                if choice == '1' or choice == "vanilla":
                    main(sentence, "vanilla")
                    break
                elif choice == '2' or choice == "laplace":
                    main(sentence, "laplace")
                    break
                elif choice == '3' or choice == "unk":
                    main(sentence, "UNK")
                    break
                elif choice == '0' or choice == "returntomainmenu":
                    break
                else:
                    print("Please enter a valid input")

        elif choice == '5' or choice == "finishasentence":
            sentence = input("Enter the first part of your sentence ")
            while True:
                print("Choose a flavour:")
                print("1) Vanilla")
                print("2) Laplace")
                print("3) UNK")
                print("0) Return to main menu")
                choice = str(input())
                choice = choice.replace(" ", "").lower()
                if choice == '1' or choice == "vanilla":
                    continueSentence(sentence, "vanilla")
                    break
                elif choice == '2' or choice == "laplace":
                    continueSentence(sentence, "laplace")
                    break
                elif choice == '3' or choice == "unk":
                    continueSentence(sentence, "UNK")
                    break
                elif choice == '0' or choice == "returntomainmenu":
                    break
                else:
                    print("Please enter a valid input")
        elif choice == '6' or choice == "testmodels":
            while True:
                print("Choose a flavour:")
                print("1) Vanilla")
                print("2) Laplace")
                print("3) UNK")
                print("0) Return to main menu")
                choice = str(input())
                choice = choice.replace(" ", "").lower()
                if choice == '1' or choice == "vanilla":
                    testModels("vanilla")
                    break
                elif choice == '2' or choice == "laplace":
                    testModels("laplace")
                    break
                elif choice == '3' or choice == "unk":
                    testModels("unk")
                    break
                elif choice == '0' or choice == "returntomainmenu":
                    break
                else:
                    print("Please enter a valid input")
        elif choice == '7' or choice == "autofilldatafolder":
            createLexicon()
            splitCorpus()
            buildModel(1, "vanilla")
            buildModel(2, "vanilla")
            buildModel(3, "vanilla")
            buildModel(1, "laplace")
            buildModel(2, "laplace")
            buildModel(3, "laplace")
            buildModel(1, "UNK")
            buildModel(2, "UNK")
            buildModel(3, "UNK")
        elif choice == '0' or choice == "exit":
            print("Exiting Application...")
            exit()
        else:
            print("Please enter a valid input")
