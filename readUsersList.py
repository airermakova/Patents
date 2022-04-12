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
nltk.download('brown')
nltk.download('universal_tagset')
from nltk import word_tokenize,pos_tag
from nltk.chunk import conlltags2tree, tree2conlltags
from pprint import pprint
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import words
from nltk.corpus import conll2000, conll2002

stemmer = SnowballStemmer("english")
pattern = 'NP: {<DT>?<JJ>*<NN>}'


def getDataFromFile(fileName):
    users = []        
    try:
       word_file = open (fileName, "r", encoding='utf-8')
       print("file object created")
       for l in word_file:
           users.append(l.replace('\r', '').replace('\n', ''))
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

def checkMarkedArrayPresence(phrases, users):
    checkUsers = False
    pr = []
    wr = []
    finArr = []
    cancelId = True
    for phrase in phrases:
        #print(phrase)
        cancelId == True
        nltk_tags = pos_tag(word_tokenize(phrase))
        iob_tagged = tree2conlltags(nltk_tags)    
        for user in users:
            if user in phrase:
                cancelId = False
        if cancelId == True:
            for iob in iob_tagged:
                iob[2] = "O"
        finArr.append(iob_tagged)
    return finArr              
                
             
            

def writeResultFile(finalArray):
    f = open("taggedPatent.txt", "a")
    for arr in finalArray:
        f.write(' '.join(str(s) for s in arr) + "\n")  
         

users = []
users = getDataFromFile("usersList.txt")
#print(users)

phrases = []
phrases = getWordsFromFile("Trialdocu.txt")

fin = checkMarkedArrayPresence(phrases, users)

writeResultFile(fin)
print(fin)
