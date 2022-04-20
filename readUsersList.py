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

def getDataFromFile(fileName):
    users = []        
    try:
       word_file = open (fileName, "r", encoding='utf-8')
       print("file object created")
       for l in word_file:
           users.append(l.replace('\r', '').replace('\n', ''))
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
    onlyUsers = []
    phrasesArr=[]
    cancelId = True
    for phrase in phrases:
        cancelId = True
        nltk_tags = pos_tag(word_tokenize(phrase))  
        iob_tagged = tree2conlltags(nltk_tags) 
        userFound = False
        for user in users:
            ind = phrase.find(user)
            if ind>0:
                us = user.split(" ")
                finArr=markUser(iob_tagged, us)
                allowAp = False
                for w in finArr:
                    if w[2] == "B" or w[2]=="I":
                        allowAp = True
                if allowAp == True:
                    onlyUsers.append(finArr)          
    return onlyUsers
                
def markUser(phrase,user):
    finTuple = []
    users = []    
    for ph in phrase:
        found = False
        nonFirst = False
        for u in user:            
            if ph[0] == u and ph[1]=="NN":
                print(user)  
                if user not in users:
                    users.append(user)              
                ls = list(ph)
                if len(user)>1:
                    if nonFirst == False:
                        ls[2]="B"
                        nonFirst = True
                    else:
                        ls[2]="I"
                else:
                    ls[2]="B"
                    nonFirst = True

                finTuple.append(tuple(ls))
                found = True
        if found == False:
            finTuple.append(ph)   
    writeUsersFile(users)  
    return finTuple
 

def writeResultFile(finalArray):
    f = open("taggedPatent.txt", "w")
    for arr in finalArray:
        f.write(' '.join(str(s) for s in arr) + "\n\n\n")  
         
def writeUsersFile(finalArray):
    f = open("onlyUsers.txt", "a")
    for arr in finalArray:
        f.write(' '.join(str(s) for s in arr) + "\n")  


users = []
users = getDataFromFile("usersList.txt")
#print(users)

phrases = []
phrases = getWordsFromFile("Trialdocu.txt")

f = open("onlyUsers.txt", "w")
f.close()

fin = checkMarkedArrayPresence(phrases, users)

writeResultFile(fin)

