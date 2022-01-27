data = ""

def getWordsFromFile(fileName, prepositions, splitSign):
    words = ""
    try:
       with open(fileName, 'r') as file:
           data = file.read()
       words = data
       for preposition in prepositions:
           words = words.replace(preposition,"")
       wordsArray = words.split(splitSign)
       return wordsArray
    except:
      print("Error in reading " + fileName)
      exit()

prepositions=[".",",",":",";","-","(",")","\n","<",">", " of "," and "," as ","\n","[","]"]

words = getWordsFromFile("AnatomyAdgectives.txt", prepositions, " ")
f = open("AnatomyAdgectivesSet.txt", "w")
for word in words:
    f.write(word + "\n")
f.close()

words = getWordsFromFile("AnatomyNouns.txt", prepositions, " ")
f = open("AnatomyNounsSet.txt", "w")
for word in words:
    f.write(word + "\n")
f.close()

def getIllnesses(fileName, prepositions, splitSign):
    finalArray=[]
    try:
       with open(fileName, 'r') as file:
           data = file.read()
       wordsArray = data.splitlines()
       for words in wordsArray:
           for preposition in prepositions:
               words = words.replace(preposition,"")
           items = words.split(splitSign)
           for item in items:
              srs = item.split("-")
              for sr in srs:
                  finalArray.append(sr)
       return finalArray
    except:
      print("Error in reading " + fileName)
      exit()

prepositions=["also", "early","see ",",","(",")","'","[","]","â€"]
words = getIllnesses("IllnessesNouns.txt",prepositions,"”")
f = open("IllnessesNounsSet.txt", "w")
for word in words:
    if len(word)>3:
        f.write(word + "\n")
f.close()