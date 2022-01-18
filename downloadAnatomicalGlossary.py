# importing required modules
import PyPDF2
	
# creating a pdf file object
pdfFileObj = open('AnatomyGlossary.pdf', 'rb')
	
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
# clean text from abbreviations
str = str.replace("'", "")
str = str.replace("L.", "")
str = str.replace("G.", "")
str = str.replace(" ", ":")
buf = str.splitlines()

bufSize = len(buf)
finBuf = ""
for i in range(0, bufSize):
    ind = buf[i].find("=")
    if ind>=0:
        finBuf +=buf[i].split("=")[0]
        

# closing the pdf file object
pdfFileObj.close()

prepositions=["on","an","in","with","for","to","of","is","a","the","this","and","or","than","then","beside","moreover","over","infront","behind",".",",",";","-","(",")"]
for preposition in prepositions:
   finBuf = finBuf.replace("preposition", "") 

finBuf = finBuf.replace(":::", ":")
finBuf = finBuf.replace("::", ":")
print(finBuf)
# write anathomy golden set
f = open("anatomySet.txt", "a")
f.write(finBuf)
f.close()
