# importing required modules
import PyPDF2
	
def readFileText(fileName, replaceSpacesAndAbr = True, splitLines = True):
    # creating a pdf file object
    pdfFileObj = open(fileName, 'rb')
	
    # creating a pdf reader object
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
	
    # printing number of pages in pdf file
    numPages = pdfReader.numPages
    print(pdfReader.numPages)
    str = ""
    for i in range(0, numPages):
        # creating a page object
        pageObj = pdfReader.getPage(i)	
        # extracting text from page
        str += pageObj.extractText()
    # closing the pdf file object
    pdfFileObj.close()
    if replaceSpacesAndAbr:
        # clean text from abbreviations
        str = str.replace("'", "")
        str = str.replace("L.", "")
        str = str.replace("G.", "")    
        str = str.replace(" ", ":")
    if splitLines:
        buf = str.splitlines()    
        return buf
    return str

def cleanFromStopWords(finBuf):
    prepositions=["on","an","in","with","for","to","of","is","a","the","this","and","or","than","then","beside","moreover","over","infront","behind",".",",",";","-","(",")"]
    for preposition in prepositions:
       finBuf = finBuf.replace("preposition", "") 
    return finBuf

def writeAnathomyGoldenSet(finBuf):
    # write anathomy golden set
    f = open("anatomySet.txt", "a")
    f.write(finBuf)
    f.close()

# read AnatomyGlossary.pdf
buf = readFileText('AnatomyGlossary.pdf')
bufSize = len(buf)
finBuf = ""
for i in range(0, bufSize):
    ind = buf[i].find("=")
    if ind>=0:
        finBuf +=buf[i].split("=")[0]
cleanStr = cleanFromStopWords(finBuf)   
cleanStr = cleanStr.replace(":::", ":")
cleanStr = cleanStr.replace("::", ":")
writeAnathomyGoldenSet(cleanStr)

# read PhysiologyGlossary.pdf
buf = readFileText('PhysiologyGlossary.pdf')
bufSize = len(buf)
finBuf = ""
for i in range(0, bufSize):
    if "," not in buf[i] and "=" not in buf[i] and "." not in buf[i] and "-" not in buf[i] and ";" not in buf[i]:
        tst = buf[i].split(":")
        if len(tst) == 1: 
            finBuf += tst[0]+":"
writeAnathomyGoldenSet(finBuf)

str = readFileText("cognitiveGlossary.pdf", False, False)
buf = str.split(".")
bufSize = len(buf)
finBuf = ""
for i in range(0, bufSize):
    testStr = buf[i].split(":")[0]
    testBuf = testStr.split(" ")
    if len(testBuf)<=2:
       for y in range(0, len(testBuf)):
           newstring = ''.join([i for i in testBuf[y] if not i.isdigit()])
           if len(newstring)>1:
               finBuf += newstring + ":"
finBuf = finBuf.replace('\n', ':').replace('\r', ':').replace(" ",":")
writeAnathomyGoldenSet(finBuf)

