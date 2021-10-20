Inside of the British National Corpus, Baby edition one can find the corpus that this project is based on.
Inside of the Data folder one can find all the generated results, such as the models.
Inside of the Scripts folder one can find all the python files.

Before making use of the python files make sure that python3 is installed on your device along with the nltk library. To download the nltk library simple use the command "pip install nltk".

There are 7 python files located inside of the script folder. The main.py provides a user interfact to make use of the other python files.
The other 6 python files can also be accessed directly from by the commands shown below:

To run main.py use the command: python3 main.py
To run lexiconBuilder.py use the command: python3 lexiconBuilder.py (Used to build the lexicon)
To run coprusSplitter.py use the command: python3 coprusSplitter.py (Used to create the training and testing sets)
To run languageModelBuilder.py use the command: python3 languageModelBuilder.py n flavour (Used to create a particular model)
Where:
n = 1 --> Unigram
n = 2 --> Bigram
n = 3 --> Trigram
flavour can be equal to “vanilla” or “laplace” or “unk”
To run calculateSentenceProbability.py use the command: python3 calculateSentenceProbability.py “Your sentence” flavour (Used to calculate the probability of the entered sentence)
To run continueMySentence.py use the command: python3 continueMySentence.py “your string” flavour (Used to continue the entered sentence)
To run modelTester.py use the command: python3 modelTester.py flavour (Used to test the models)
