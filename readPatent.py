data = ""
prepositions=["on","an","in","with","for","to","of","is","a","the","this","and","or","than","then","beside","moreover","over","infront","behind",".",",",":",";","-"]

def getWordsFromFile(fileName):
    words = []
    try:
       with open(fileName, 'r') as file:
           data = file.read().replace('\n', ' ')
       wordsArray = data.split(" ")
       for i in range(0, len(wordsArray)):
           canAdd = True
           for preposition in prepositions:
              if wordsArray[i] == preposition:
                  canAdd = False
           if canAdd == True:
               words.append(wordsArray[i])     
       return words
    except:
      print("Error in reading " + fileName)
      exit()

weightedWords = getWordsFromFile("humanBodyRelatedWords.txt")
patentWords = getWordsFromFile("PatentExample.txt")
patentGoldenSetWeigth1 = []
patentGoldenSetWeigth2 = []

for word in patentWords:
    ret_value = word in weightedWords
    if ret_value: 
        exist = word in patentGoldenSetWeigth1
        if exist==False:
            patentGoldenSetWeigth1.append(word)
    else:
        patentGoldenSetWeigth2.append(word)
        

print("patent significant words - ")
print(patentWords)
print("human body related words - ")
print(weightedWords)
print("Golden Set Weigth 1")
print(patentGoldenSetWeigth1)
print("Golden Set Weigth 2")
print(patentGoldenSetWeigth2)

f = open("goldenSetWeight1.txt", "a")
for word in patentGoldenSetWeigth1:
    f.write(word + ";")
f.close()

f = open("goldenSetWeight2.txt", "a")
for word in patentGoldenSetWeigth2:
    f.write(word + ";")
f.close()
