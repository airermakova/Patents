from flair.data import Corpus
from flair.datasets import ColumnCorpus
from flair.embeddings import WordEmbeddings, StackedEmbeddings
from flair.models import SequenceTagger
from flair.trainers import ModelTrainer
from flair.data import Sentence
import re
import nltk
import numpy
import random
import codecs
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

phrases = []
fphrases = []
users = []
model = SequenceTagger.load("C:/Users/airer/Documents/Pisa/Classifier/trainer/final-model.pt")

#TO GET PHRASES
def getPhrasesFromFile(fileName, st, fin):
    phrases= []  
    finArr = []  
    tokenized_phrases = []
    try:
       with codecs.open(fileName, 'r', "utf-8") as file:
           phrases = file.read().split(".")
       for i in range(st,fin):
           finArr.append(phrases[i])
       return finArr
    except:
      print("Error in reading " + fileName)
      exit()

#TO MARK USERS AS WE HAVE DONE FOR TRAIN SET

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

#TO MARK USERS IN PHRASES 

def markUsers(phrases):
    finArr = []
    for phrase in phrases:
       finArr.append(getUsersFromNN(phrase)) 
    return finArr    

   
def getUsersFromNN(phrase):
    # create example sentence
    sentence = Sentence(phrase)
    # predict tags and print
    model.predict(sentence)
    sent = sentence.to_tagged_string()
    onlusers = sent.split("[")
    #create tuples
    onlyUsers = []
    tupleArr = onlusers[1].split(",")
    for tp in tupleArr: 
        t = tp.split("/")
        if len(t)>1:
            if t[1] == "<unk>" or t[1] == "<unk>]":
                t[1] = "O"
            onlyUsers.append(tuple(t))
    return onlyUsers

#TO STORE MARKED PHRASES IN FINAL FILE

def writeUsersFile(finalArray):
    f = open("markedPhrases.txt", "w")
    for arr in finalArray:
        f.write(' '.join(str(s) for s in arr) + "\n\n")  


def writeOnlySimpleUsersFile(finalArray):
    f = open("markedSimpleUsersOnly.txt", "w")
    for arr in finalArray:
        found = False
        for s in arr:
            if s[1] == "B":
                found = True
        if found == True:
            f.write(' '.join(str(s) for s in arr) + "\n\n")  



def writeOnlyComUsersFile(finalArray):
    f = open("markedComUsersOnly.txt", "w")
    for arr in finalArray:
        found = False
        for s in arr:
            if s[1] == "I":
                found = True
        if found == True:
            f.write(' '.join(str(s) for s in arr) + "\n\n")

#MAIN SCRIPT

phrases = getPhrasesFromFile("testData.txt", 0, 1000)
print("Taken phrases - ")
print(len(phrases))
users=markUsers(phrases)
print(users)
writeUsersFile(users)
writeOnlySimpleUsersFile(users)
writeOnlyComUsersFile(users)