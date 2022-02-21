import re
import nltk
import numpy
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
from nltk import word_tokenize,pos_tag


tokenized_phrases = []

def getWordsFromFile(fileName):
    phrases= []    
    try:
       with open(fileName, 'r') as file:
           phrases = file.read().split(".")
       for phrase in phrases:
           #tokenized_phrases.append(re.split(r'\W+', phrase))
           tokenized_phrases.append(word_tokenize(phrase))
       return tokenized_phrases
    except:
      print("Error in reading " + fileName)
      exit()

def markPhrases():
    f = open("taggedPhrases.txt", "a")
    for tokenized_phrase in tokenized_phrases:
        tag=pos_tag(tokenized_phrase)
        ne_tree = nltk.ne_chunk(tag)
        line = ' '.join(str(x) for x in ne_tree)
        f.write(line + "\n")
f = open("taggedPhrases.txt", "w")
f.close()
getWordsFromFile("Phrases.txt")
markPhrases()