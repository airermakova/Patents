import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm


def getWordsFromFile(sourceFileName, destFileName):
    phrases= [] 
    tagged_Phrases = []  
    try:
        with open(sourceFileName, 'r') as file:
            data = file.read()
        f = open(destFileName, "w")
        f.write(data)
        f.write("\n")
        doc = nlp(data)        
        for ent in doc:
            print(ent.text + " - " + ent.ent_iob_)
            f.write("(" + ent.text + "-" + ent.ent_iob_ + ")")
    except:
      print("Error in reading " + sourceFileName)
      exit()


nlp = en_core_web_sm.load()
f = open("taggedPhrases.txt", "w")
f.close()
getWordsFromFile("PatentExample.txt", "taggedPhrasesSpacy.txt")