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
goldtags = []
tags = []
cs = []
iob_tagged = []
tagged_phrases=[]
nltk_tags=[]

pattern = 'NP: {<DT>?<JJ>*<NN>}'

#MAIN FUNCTIONALITY AREA

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

def getWordsFromGoldenSet(fileName):
    tags = []
    phrases = []
    try:
        with open(fileName, 'r') as file:
            phrases = file.read().split("\n")
        for phrase in phrases:
            for word in (word_tokenize(phrase)):
                if word not in tags and len(word)>3:
                    tags.append(word) 
        return tags       
    except: 
        print("Error in reading file " + fileName)
        exit()

def recheckTaggedPhrases(tagged_phrases, tags):
    id = "O"
    prevId = "O"
    finalTags = []
    identity=[]
    for phrase in tagged_phrases:
        identity = getMarkedIdentity(phrase)
        if len(identity)==0: 
            finalTags.append(phrase)
        elif len(identity)>0:
            newphrase = overwriteIdentity(identity, phrase, tags)
            finalTags.append(newphrase)
        else: 
            finalTags.append(phrase)
        identity=[]
    return finalTags

def writeResultFile(tokenized_phrases, iob_tagged):
    f = open("taggedPhrases.txt", "a")
    for phrase in tokenized_phrases:
        f.write(' '.join(str(s) for s in phrase) + "\n\n")    
    for iob in iob_tagged:
        f.write(' '.join(str(s) for s in iob) + "\n\n")   


#MAIN FUNCTIONALITY AREA END

#SERVICE FUNCTIONS AREA

def markIdentity(word, tags, prev):
    id = "O"
    if word in tags: 
        if prev == "O":
            id = "B"
        else: 
            id = "I"
    else: 
       id = "O"
    return id


def addGoldSetTags(final_phrases, tags): 
    tagged_words = []
    tagged_phrases = []
    id = "O"
    prevId = "O"
    for phrase in final_phrases:
        tagged_words=[]
        id="O"
        prevId = "O"
        for word in phrase:
           if "O" in word: 
                id = markIdentity(word, tags, prevId)
                prevId=id
                tagged_words.append([word[0],word[1], id])
           else: 
                tagged_words.append(word)
        tagged_phrases.append(tagged_words)
    return tagged_phrases

def cancelIdentity(phrase, id): 
    newPh = []
    wr = []
    for w in phrase:
        for i in id:
            if w[0] == i[0]:
                wr.append(w[0])
                wr.append(w[1])
                wr.append("O")
        if len(wr)>0: 
            newPh.append(wr)
        else: 
            newPh.append(w)
        wr = []
    return newPh 

def getMarkedIdentity(phrase):
    identity = []
    id = []
    for word in phrase:          
        if len(word)==3:
            if "B" in word[2]:
                if len(id)>0:
                      identity.append(id)
                      id = []
                id.append(word)
            elif "I" in word[2]:
                id.append(word)
            elif len(id)>0:
                identity.append(id)
                id = []
    return identity

def overwriteIdentity(identity, phrase, tags):
    newphrase = phrase            
    for id in identity:                
       cnt = 0
       for w in id:                     
          if w[0] in tags:
             cnt=cnt + 1             
       if cnt==0:
          newphrase = cancelIdentity(newphrase, id)
    return newphrase

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

#SERVICE FUNSTIONS AREA END


#clean log file
f = open("taggedPhrases.txt", "w")
f.close()


tokenized_phrases = getWordsFromFile("Phrases.txt")
nltk_tags = markPhrases(tokenized_phrases)
cs = createVector(nltk_tags)
iob_tagged = findNER(cs)

tags = getWordsFromGoldenSet("GoldenSet.txt")
tagged_phrases = recheckTaggedPhrases(iob_tagged, tags)
fin_phrases = addGoldSetTags(tagged_phrases, tags)
#tagged_phrases = findGoldSetTags(tokenized_phrases, tags)
writeResultFile(tokenized_phrases, fin_phrases)



    