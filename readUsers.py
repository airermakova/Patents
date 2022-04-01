import re
import nltk
import numpy
from langdetect import detect
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('conll2002')
nltk.download('conll2000')
from nltk import word_tokenize,pos_tag
from nltk.chunk import conlltags2tree, tree2conlltags
from pprint import pprint
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import words
from nltk.corpus import conll2000, conll2002


stemmer = SnowballStemmer("english")

def getDataFromFile(fileName):
    users = []    
    
    try:
       word_file = open (fileName, "r", encoding='utf-8')
       for l in word_file:
           users.append(l.replace('\r', '').replace('\n', ''))
       print("Number of elements added in array")
       print(len(users))
       return users
    except:
      print("Error in reading " + fileName)
      if len(users)>0:
          print(users[len(users)-1])
      exit()

def getWordsFromFile(fileName):
    phrases= []    
    tokenized_phrases = []
    try:
       with open(fileName, 'r') as file:
           phrases = file.read().split(".")
       return phrases
    except:
      print("Error in reading " + fileName)
      exit()

def checkMarkedArrayPresence(phrases, users, prop):
    checkUsers = False
    pr = []
    wr = []
    finArr = []
    for phrase in phrases:
        for p in prop:
            wroot = stemmer.stem(p)
            if wroot in phrase and wroot not in wr:
                 pr.append(p)
                 wr.append(wroot)
        if len(pr)>0:
           for u in users:
                wroot = stemmer.stem(u)
                if wroot in phrase and wroot not in wr:
                   pr.append(u)
                   wr.append(wroot)
        if len(pr)>0:
            finArr.append(pr)
            pr = []
            wr = []
    return finArr

def writeResultFile(finalArray):
    f = open("additionalUsers.txt", "a")
    for arr in finalArray:
        f.write(' '.join(str(s) for s in arr) + "\n")  
         

users = []
users = getDataFromFile("user.txt")
#print(users)

significants = []
significants = getDataFromFile("GoldenSet.txt")

phrases = []
phrases = getWordsFromFile("Phrases.txt")

fin = checkMarkedArrayPresence(phrases, users, significants)

writeResultFile(fin)
print(fin)
