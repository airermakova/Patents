import re
import nltk
import numpy
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
from nltk import word_tokenize,pos_tag
from nltk.chunk import conlltags2tree, tree2conlltags
from pprint import pprint


tokenized_phrases = []
tags = []
cs = []
iob_tagged = []
tagged_phrases=[]

pattern = 'NP: {<DT>?<JJ>*<NN>}'

def getWordsFromFile(fileName):
    phrases= []    
    tokenized_phrases = []
    try:
       with open(fileName, 'r') as file:
           phrases = file.read().split(".")
       for phrase in phrases:
           tokenized_phrases.append(word_tokenize(phrase))
       return tokenized_phrases
    except:
      print("Error in reading " + fileName)
      exit()

def markPhrases(tokenized_phrases):
    tags = []
    f = open("taggedPhrases.txt", "a")
    for tokenized_phrase in tokenized_phrases:
        tags.append(pos_tag(tokenized_phrase))
    return tags

def markIdentity(word, tags, prev):
    id = "O"
    for tag in tags:        
        if word in tag: 
            if prev == "O":
                id = "B"
            else: 
                id = "I"
        else: 
            id = "O"
    return id

def createVector(tags):
    cs = []
    #prepare parser
    cp = nltk.RegexpParser(pattern)
    for tag in tags:
        cs.append(cp.parse(tag))
    return cs

def findNER(cs):
    iob_tagged = []
    for c in cs:
       iob_tagged.append(tree2conlltags(c))
    return iob_tagged

def writeResultFile(iob_tagged):
    f = open("taggedPhrases.txt", "a")
    for iob in iob_tagged:
         f.write(' '.join(str(s) for s in iob) + "\n\n")         

def findGoldSetTags(tokenized_phrases, tags): 
    tagged_words = []
    tagged_phrases = []
    id = "O"
    prevId = "O"
    for phrase in tokenized_phrases:
        tagged_words=[]
        id="O"
        for word in phrase:
           id = markIdentity(word, tags, prevId)
           prevId=id
           tagged_words.append([word, id])
        tagged_phrases.append(tagged_words)
    return tagged_phrases



#clean log file
f = open("taggedPhrases.txt", "w")
f.close()


tokenized_phrases = getWordsFromFile("Phrases.txt")
tags = getWordsFromFile("GoldenSet.txt")
#print(tags)
#print(tokenized_phrases)
tagged_phrases = findGoldSetTags(tokenized_phrases, tags)
writeResultFile(tagged_phrases)



    