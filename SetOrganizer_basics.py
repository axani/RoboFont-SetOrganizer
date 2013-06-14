from vanilla import *
from mojo.UI import SmartSet, getSmartSets, setSmartSets, addSmartSet, removeSmartSet


# Lists and dictionaries to use
standardSets = []
standardSets_dict = {}
activeSets = []
setsToDeactivate = []
setsToSave = []
checkboxSetLink_dict = {}


# smartSet Functions
def declareAsStandard(set):
    standardSets_dict[str(set)] = set
    standardSets.append(set)

def pickUpActiveSets():
    activeSets[:] = []
    print 'picking up active sets'
    for set in getSmartSets():
        activeSets.append(set)
        print set.name, 'is active!'

def activateSet(thisSet):
    addSmartSet(thisSet)
    activeSets.append(thisSet)
    #print thisSet, ' ++ now active!'
    #print 'Active sets:', activeSets

def deactivateSet(thisSet):
    
    setsToDeactivate[:] = []
    setsToSave[:] = []

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
    #print setsToDeactivate, '-- now inactive!'
    #print 'Active sets:', activeSets

# My standard sets
set_lowercase = SmartSet({'smartSetName': 'Lowercase', 'query': 'Name MATCHES "[a-z]"'})
set_uppercase = SmartSet({'smartSetName': 'Uppercase', 'query': 'Name MATCHES "[A-Z]"'})

declareAsStandard(set_lowercase)
declareAsStandard(set_uppercase)

class setOrganizer():

    def __init__(self):

        # Create window
        self.w = Window((400,400), 'Active/Deactivate your SmartSets')

        # Create a checkbox for every standard set
        i = 0
        for key in standardSets_dict:
            setID = key
            set = standardSets_dict[key]

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
        linkedSet = standardSets_dict[linkedSetName]

        if sender.get() is 1:
            activateSet(linkedSet)

        else:
            deactivateSet(linkedSet)
        
setOrganizer()