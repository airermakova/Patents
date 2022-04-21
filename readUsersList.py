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
            us = user.split(" ")
            if ind>0:
               iob_tagged = markUser(iob_tagged, us)
        for iob in iob_tagged:
            if iob[2]=="B":
                onlyUsers.append(markUser(iob_tagged, us))          
    return onlyUsers
                
def markUser(phrase,user):
    finTuple = []
    users = []
    found = False
    if len(user)>1:
       nonFirst = False
       cnt = 0
       ucnt = 0
       for ph in phrase:
           finTuple.append(ph)
           ucnt = ucnt +1
           found = False
           for u in user: 
               if ph[0]==u:
                   found = True
           if found == True:
               cnt = cnt + 1
           else:
               cnt = cnt - 1
           if cnt == len(user)-1:              
               ls = list(phrase[ucnt-cnt-1])
               ls[2]="B"
               finTuple[ucnt-cnt-1]=tuple(ls)
               for i in range(cnt):
                   ls = list(phrase[ucnt-cnt+i])
                   ls[2]="I"
                   finTuple[ucnt-cnt+i]=tuple(ls)
               cnt = 0           
       print(finTuple)
    else:
        print(user)
        for ph in phrase:
           finTuple.append(ph)         
           if ph[0] == user[0] and ph[1][0]=="N":  
               if user[0] not in users:
                    users.append(user[0])              
               ls = list(ph)
               ls[2]="B"
               finTuple[len(finTuple)-1] = (tuple(ls))                    
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
#print(fin)
writeResultFile(fin)

