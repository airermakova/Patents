import re


def getWordsFromFile(fileName):
    phrases= []
    tokenized_phrases = []
    try:
       with open(fileName, 'r') as file:
           phrases = file.read().split(".")
       for phrase in phrases:
           tokenized_phrases.append(re.split(r'\W+', phrase))
       print(tokenized_phrases)
       return tokenized_phrases
    except:
      print("Error in reading " + fileName)
      exit()

getWordsFromFile("Phrases.txt")
