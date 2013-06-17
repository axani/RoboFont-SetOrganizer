import os
import json


# Get all setFiles
mySetFileNames = []

for file in os.listdir('mySets'):
    if file != '00-README.txt' and file.endswith(".txt"):
        mySetFileNames.append(file)

# print mySetFileNames


# Create dictionary of all set data
allSetData = {}

for fileName in mySetFileNames:
    file = open('mySets/' + fileName)
    
    fileData = json.load(file)
    fileName = fileName.replace('.txt', '')
    allSetData[fileName] = fileData
    
    file.close

print allSetData

# set_lowercase = SmartSet({'smartSetName': 'Lowercase', 'query': 'Name MATCHES "[a-z]"'})