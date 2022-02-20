import re
tokenized_phrases = []

def getWordsFromFile(fileName):
    phrases= []
    
    try:
       with open(fileName, 'r') as file:
           phrases = file.read().split(".")
       for phrase in phrases:
           tokenized_phrases.append(re.split(r'\W+', phrase))
       return tokenized_phrases
    except:
      print("Error in reading " + fileName)
      exit()

def markPhrases():
    f = open("taggedPhrases.txt", "a")
    for tokenized_phrase in tokenized_phrases:
        for word in tokenized_phrase:
            if len(word)>0: 
                word = word + "(N)"
                f.write(word + " ")
        f.write("\n")
f = open("taggedPhrases.txt", "w")
f.close()
getWordsFromFile("Phrases.txt")
markPhrases()