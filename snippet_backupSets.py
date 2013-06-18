from vanilla import *
from mojo.UI import SmartSet, getSmartSets, setSmartSets, addSmartSet, removeSmartSet
import os
import json
import time
import datetime



def getActiveSets():
    # Clear list of activeSets to start fresh
    activeSets = []
    for set in getSmartSets():
        activeSets.append(set)
    
    return activeSets

def backupSetData(set):
    folder = 'backuppedSets'
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H-%M_')
    filename = timestamp + set.name + '.txt'
    file = open(folder + '/' + filename, 'w+')
    
    nameString = '"smartSetName": "' + str(set.name) + '"'
    queryString = '"query": "' +  str(set.query) + '"'
    dataString = '{\n' +  nameString + ',\n' + queryString + '\n}'

    file.write(dataString)
    file.close()


currentlyActiveSets = getActiveSets() 
for set in currentlyActiveSets:
    backupSetData(set)
