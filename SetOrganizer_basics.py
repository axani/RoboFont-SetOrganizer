from vanilla import *
from mojo.UI import SmartSet, getSmartSets, setSmartSets, addSmartSet, removeSmartSet
import os
import json
import time
import datetime


# Lists and dictionaries to use
activeSets = []
setsToDeactivate = []
setsToSave = []
checkboxSetLink_dict = {}

allExternalSets_dict = {}
activeExternalSets = []

# smartSet Functions

def updateActiveSetList():
    activeSets[:] = []
    for set in getSmartSets():
        activeSets.append(set)

    # print 'ActiveSets updated. Current active sets are:', activeSets

def activateSet(thisSet):
    addSmartSet(thisSet)
    activeSets.append(thisSet)
    # print thisSet, 'was actived!'

def deactivateSet(thisSet):
    # Loop through all current active sets
    for set in activeSets:
        # Check every active set, if it is the one to deactivate
        if set.name == thisSet.name and set.query == thisSet.query:
            setsToDeactivate.append(set)
        else:
            # if not put it on the save list
            setsToSave.append(set)
    # After the loop is finished, clear the list of active sets
    activeSets[:] = []
    # Put the saved sets in it
    activeSets.extend(setsToSave)
    setSmartSets(setsToSave)
    # print setsToDeactivate, 'was deactivated!'

class loadExternalSets():

    def __init__(self):
        externalFolder = 'SmartSets'
            
        for filename in self.getSetFilenameList(externalFolder):
            thisSetData = self.getSetData(externalFolder, filename)
            thisSmartSet = SmartSet(thisSetData)
            allExternalSets_dict[filename] = thisSmartSet

    def getSetFilenameList(self, folder):
        readmeFile = '00-README.txt'
        mySetFilenames = []
        for file in os.listdir(folder):
            if file.endswith('.txt') and file != readmeFile:
                mySetFilenames.append(file)

        return mySetFilenames

    def getSetData(self, folder, filename):
        file = open(folder + '/' + filename)
        fileData = json.load(file)
        file.close

        return fileData

def saveThisSet(set):
    # Backups the set in a folder where it can be copied to the regular SmartSet folder
    folder = 'SmartSets_Backup'
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H-%M_')
    filename = timestamp + set.name + '.txt'
    file = open(folder + '/' + filename, 'w+')
    
    nameString = '"smartSetName": "' + str(set.name) + '"'
    queryString = '"query": "' +  str(set.query).replace('"', "'") + '"'
    dataString = '{\n' +  nameString + ',\n' + queryString + '\n}'

    file.write(dataString)
    file.close()

def isExternal(set):
    for externalSetID in allExternalSets_dict:
        thisSet = allExternalSets_dict[externalSetID]        
        if set.name == thisSet.name and set.query == thisSet.query:
            return externalSetID

class setOrganizer():

    def __init__(self):

        updateActiveSetList()
        activeSetsNow = activeSets
        
        if activeSetsNow:
            for set in activeSetsNow:
                if isExternal(set):
                    activeExternalSets.append(isExternal(set))
                else:
                    # Deals with the problem that intern created sets disappear after the restart of the script.
                    saveThisSet(set)


        # Create window
        self.w = Window((150,400), 'Active/Deactivate your SmartSets')

        # ! - This part needs a clean up!
        currentRow = 0
        self.w.caption_externalSets = TextBox((10, 10 + currentRow, 0, 0), 'External SmartSets')

        for item in allExternalSets_dict:
            currentRow = self.createCheckbox(item, allExternalSets_dict, currentRow)
        
        numberOfRows = currentRow
        self.w.box_externalSets = Box((10, 30, -10, 15+25*numberOfRows))
        
        setsInFirstPart = numberOfRows
        currentRow = numberOfRows + 2
        beginNextPart = 25*numberOfRows
        numberOfRows = 1
        self.w.caption_internalSets = TextBox((10, 62+beginNextPart, 0, 0), 'Internal SmartSets')
        
        for item in activeSetsNow:
            currentRow = self.createCheckbox(item, activeSetsNow, currentRow)

        numberOfRows = currentRow - setsInFirstPart -2
        
        print numberOfRows
        self.w.box_internalSets = Box((10, 82+beginNextPart, -10, 12+25*numberOfRows))

        # Open window
        self.w.open()

    def createCheckbox(self, key, dataToLoop, row):
            
        # Check if list or dictionary
        if type(dataToLoop) is dict:
            set = dataToLoop[key]
            setID = key
            notSureIfActive = True
        
        else:
            # ! - ActiveSets/ActiveSetsnow sollte ebenfalls ein dictionary wie die anderen SmartSetListen sein
            set = key
            setID = str(key)
            notSureIfActive = False

        # Set checkBoxValue and checkBoxType
        if isExternal(set) and notSureIfActive:
            if setID in activeExternalSets:
                checkBoxValue = True
            
            else:
                checkBoxValue = False
            
            checkBoxLinkDestination = setID
            callbackDestination = self.checkBoxCallback_external
            permissionToBuild = True
        
        elif isExternal(set):
            permissionToBuild = False
            return row

        else:
            checkBoxValue = True
            checkBoxLinkDestination = set
            callbackDestination = self.checkBoxCallback_internal
            permissionToBuild = True
        
        if permissionToBuild:
            checkboxObject = CheckBox((20, 40+25*row, -10, -10), " %s" % set.name, callback=callbackDestination, value = checkBoxValue)
            setattr(self.w, setID, checkboxObject)
        
            # Link checkbox with Set
            checkboxSetLink_dict[checkboxObject] = checkBoxLinkDestination

            row = row + 1 
            return row


    def handleCallback(self, sender, linkedSet):
        setsToDeactivate[:] = []
        setsToSave[:] = []

        if sender.get() is 1:
            activateSet(linkedSet)

        else:
            deactivateSet(linkedSet)


    def checkBoxCallback_external(self, sender):
        # Get linked set of checkbox
        linkedSetName = checkboxSetLink_dict[sender]
        linkedSet = allExternalSets_dict[linkedSetName]
        self.handleCallback(sender, linkedSet)

    def checkBoxCallback_internal(self, sender):
        # Get linked set of checkbox
        linkedSet = checkboxSetLink_dict[sender]
        self.handleCallback(sender, linkedSet)

        


# Run Set Organizer

loadExternalSets()     
setOrganizer()
