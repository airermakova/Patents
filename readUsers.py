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
        words = phrase.split(" ")
        cnt = 0
        for w in words:
            #print(w)
            for p in prop:
                wroot = stemmer.stem(p)
                if wroot in w and wroot not in wr:
                    pr.append(p)
                    wr.append(wroot)
            if len(pr)>0 and cnt>0 and cnt<len(words)-2:
                for u in users:
                    wroot = stemmer.stem(u)
                    if wroot in words[cnt-1] or wroot in words[cnt+1] and wroot not in wr:
                        pr.append(u)
                        wr.append(wroot)
            cnt = cnt + 1
        
            if len(pr)>1:
                tp =  nltk.pos_tag(pr)
                nounCnt= 0
                adCount = 0
                for t in tp:
                    if 'NN' in t[1]:
                        nounCnt=nounCnt + 1
                    elif "PR" in t[1]:
                        adCount = adCount+1
                if nounCnt == 1 and adCount==0:
                    print(pr)
                    finArr.append(pr)
                pr = []
                wr = []
        cnt = 0
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
phrases = getWordsFromFile("Trialdocu.txt")

fin = checkMarkedArrayPresence(phrases, users, significants)

writeResultFile(fin)
print(fin)
