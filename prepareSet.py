# Import Module
import os
import codecs

# Folder Path
sourcepath=r"C:\Users\airer\Downloads\patents_data-20220413T200348Z-001\patents_data"
destpath = r"C:\Users\airer\Documents\Pisa\Classifier"

# Change the directory
os.chdir(sourcepath)

# Read text File

trainfile = os.path.join(destpath, "testData.txt")
dstfile = codecs.open(trainfile, "a", "utf-8")


def read_text_file(file_path):
	with open(file_path, "r", encoding='utf8', errors='ignore') as f:
		dstfile.write(f.read())


# iterate through all file
for file in os.listdir():
	# Check whether file is in text format or not
	if file.endswith(".txt"):
		file_path = f"{sourcepath}\{file}"

		# call read text file function
		read_text_file(file_path)

dstfile.close()