from vanilla import *
from mojo.UI import SmartSet, getSmartSets, setSmartSets, addSmartSet, removeSmartSet
import os
import json
import time
import datetime


# Lists and dictionaries to use
allSetData = {}
activeSets = []
setsToDeactivate = []
setsToSave = []
checkboxSetLink_dict = {}

allExternalSets_dict = {}
activeExternalSets = []
activeInternalSets = []


# smartSet Functions

def updateActiveSetList():
    activeSets[:] = []
    for set in getSmartSets():
        activeSets.append(set)
        print set.name, 'is active!'

    print 'ACTIVESETS:', activeSets
    # return activeSets

def activateSet(thisSet):
    addSmartSet(thisSet)
    activeSets.append(thisSet)
    print thisSet, ' ++ now active!'
    print 'Active sets:', activeSets

def deactivateSet(thisSet):
    # Loop through all current active sets
    for set in activeSets:
        # Check every active set, if it is the one to deactivate
        print 'deaktivieren: vergleiche ', set, 'und ', thisSet
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
    print setsToDeactivate, '-- now inactive!'
    print 'Active sets:', activeSets

class loadExternalSets():
    # Load all sets from external folder

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


class backupSetData():
    # Deals with the problem that a smartSet gets lost in this case:
    # When creating a smartSet in RoboFont internally and deactivating it with the Script. After a restart this particular smartSet is lost.
    # But thanks to this method it gets saved in a backup-folder
    # If you want to restore it you have to put it in the main sets-folder.

    def __init__(self):

        # Get active Sets
        activeSets = []
        for set in getSmartSets():
            activeSets.append(set)

        internSets_active, externSets_active = self.compareWithExternSets()
        
        for set in internSets_active:
            self.backupInternSets(set)

    def compareWithExternSets(self):
        print 'Coming soon …'
        return 'Interne Sets, die aktiv sind', 'externe Sets, die aktiv sind'

    def backupInternSets(self, set):
        print set
        # folder = 'SmartSets_Backup'
        # timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H-%M_')
        # filename = timestamp + set.name + '.txt'
        # file = open(folder + '/' + filename, 'w+')
        
        # nameString = '"smartSetName": "' + str(set.name) + '"'
        # queryString = '"query": "' +  str(set.query) + '"'
        # dataString = '{\n' +  nameString + '\n' + queryString + '\n}'

        # file.write(dataString)
        # file.close()

def saveThisSet(set):
    folder = 'SmartSets_Backup'
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H-%M_')
    filename = timestamp + set.name + '.txt'
    file = open(folder + '/' + filename, 'w+')
    
    nameString = '"smartSetName": "' + str(set.name) + '"'
    queryString = '"query": "' +  str(set.query).replace('"', "'") + '"'
    dataString = '{\n' +  nameString + '\n' + queryString + '\n}'
    print queryString

    file.write(dataString)
    file.close()

def isExternal(set):
    print 'set:', set
    for externalSetID in allExternalSets_dict:
        thisSet = allExternalSets_dict[externalSetID]
        if set.name == thisSet.name and set.query == thisSet.query:
            return externalSetID
        else:
            return False

class setOrganizer():

    def __init__(self):

        updateActiveSetList()
        activeSetsNow = activeSets
        
        if activeSetsNow:
            for set in activeSetsNow:
                if isExternal(set):
                    activeExternalSets.append(isExternal(set))
                    print 'active external set: ', set
                else:
                    print set, 'saved!'
                    saveThisSet(set)


        # Create window
        self.w = Window((400,400), 'Active/Deactivate your SmartSets')

        # Create a checkbox for every standard set
        i = 0
        for key in allExternalSets_dict:
            print 'allExternalSets_dict key', key
            setID = key
            set = allExternalSets_dict[key]

            # Check if set is active
            if setID in activeExternalSets:
                checkBoxvalue = True
            else:
                checkBoxvalue = False

            # Create checkbox
            checkboxObject = CheckBox((10, 10+30*i, -10, -10), " %s" % set.name, callback=self.checkBoxCallback, value = checkBoxvalue)
            setattr(self.w, setID, checkboxObject)
            
            # Link checkbox with Set
            checkboxSetLink_dict[checkboxObject] = setID

            i += 1

        # Create checkbox for every internal active set
        for key in activeSetsNow:
            print 'activeSetsNow key:', key
            setID = str(key)
            set = key

            if not isExternal(set):
                print 'this setID is not in activeExternalSets: ', setID

                # Create checkbox
                checkboxObjectInternal = CheckBox((10, 10+30*i, -10, -10), " %s" % set.name, callback=self.checkBoxCallback_internal, value = True)
                setattr(self.w, setID, checkboxObjectInternal)

                # Link checkbox with Set
                checkboxSetLink_dict[checkboxObjectInternal] = set

                i += 1

        # Open window
        self.w.open()

    def checkBoxCallback(self, sender):
 
        # Get linked set of checkbox
        linkedSetName = checkboxSetLink_dict[sender]
        linkedSet = allExternalSets_dict[linkedSetName]

        setsToDeactivate[:] = []
        setsToSave[:] = []

        if sender.get() is 1:
            activateSet(linkedSet)

        else:
            deactivateSet(linkedSet)
            print 'deaktivieren: ', linkedSet, type(linkedSet)

    def checkBoxCallback_internal(self, sender):

        # Get linked set of checkbox
        linkedSet = checkboxSetLink_dict[sender]

        setsToDeactivate[:] = []
        setsToSave[:] = []

        if sender.get() is 1:
            activateSet(linkedSet)

        else:
            deactivateSet(linkedSet)
            print 'deaktivieren internal: ', linkedSet, type(linkedSet)

# Run Set Organizer

loadExternalSets()

#backupSetData()        
setOrganizer()
