from vanilla import *
from mojo.UI import SmartSet, getSmartSets, setSmartSets, addSmartSet, removeSmartSet
import os
import json


# Lists and dictionaries to use
allSetData = {}
allSmartSets_obj = []
allSmartSets_dict = {}
activeSets = []
setsToDeactivate = []
setsToSave = []
checkboxSetLink_dict = {}


# smartSet Functions

def getFilelist():
    mySetFileNames = []
    folder = 'mySets'
    readmeFile = '00-README.txt'
    for file in os.listdir(folder):
        if file.endswith('.txt') and file != readmeFile:
           mySetFileNames.append(file)

    # print mySetFileNames
    return mySetFileNames 

def createAllSetDataFromFiles():
    setNames = getFilelist()

    for fileName in setNames:
        file = open('mySets/' + fileName)
        
        fileData = json.load(file)
        fileName = fileName.replace('.txt', '')
        allSetData[fileName] = fileData
        
        file.close

    print 'allSetData: ', allSetData
    return allSetData

def generateSmartSets(setDict):
    for set in setDict:
        newSet = SmartSet(setDict[set])
        allSmartSets_dict[str(newSet)] = newSet
        allSmartSets_obj.append(newSet)

    print 'allSmartSets_dict: ', allSmartSets_dict
    print 'allSmartSets_obj: ', allSmartSets_obj

def pickUpActiveSets():
    # ! - Currently not in use
    activeSets[:] = []
    print 'picking up active sets'
    for set in getSmartSets():
        activeSets.append(set)
        print set.name, 'is active!'

def activateSet(thisSet):
    addSmartSet(thisSet)
    activeSets.append(thisSet)
    print thisSet, ' ++ now active!'
    print 'Active sets:', activeSets

def deactivateSet(thisSet):
    # Loop through all current active sets
    for set in activeSets:
        # Check every active set, if it is the one to deactivate
        if set is thisSet:
            setsToDeactivate.append(set)
        else:
            # if not put it on the save list
            setsToSave.append(set)
    # After the loop is finished, clear the list of active sets
    activeSets[:] = []
    # Put the saved sets in it
    activeSets.extend(setsToSave)
    setSmartSets(setsToSave)
    print setsToDeactivate, '-- now inactive!'
    print 'Active sets:', activeSets


class setOrganizer():

    def __init__(self):

        # Create window
        self.w = Window((400,400), 'Active/Deactivate your SmartSets')

        # Create a checkbox for every standard set
        i = 0
        for key in allSmartSets_dict:
            setID = key
            set = allSmartSets_dict[key]

            # Create checkbox
            checkboxObject = CheckBox((10, 10+30*i, -10, -10), " %s" % set.name, callback=self.checkBoxCallback, value=False)
            setattr(self.w, setID, checkboxObject)
            
            # Link checkbox with Set
            checkboxSetLink_dict[checkboxObject] = setID

            i += 1

        # Open window
        self.w.open()

    def checkBoxCallback(self, sender):
 
        # Get linked set of checkbox
        linkedSetName = checkboxSetLink_dict[sender]
        linkedSet = allSmartSets_dict[linkedSetName]

        setsToDeactivate[:] = []
        setsToSave[:] = []

        if sender.get() is 1:
            activateSet(linkedSet)

        else:
            deactivateSet(linkedSet)

# Run Set Organizer

allSmartSets = createAllSetDataFromFiles()
generateSmartSets(allSmartSets)        
setOrganizer()