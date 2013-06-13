from vanilla import *
from mojo.UI import SmartSet, getSmartSets, setSmartSets, addSmartSet, removeSmartSet

# My standard sets
# ? - Koennte ausgelagert werden

standardSets = []
standardSets_dict = {}

set_ipa = SmartSet()
set_ipa.name = 'Ipanema'
set_ipa.query = 'Name MATCHES "[a-z]"'

standardSets_dict['set_ipa'] = set_ipa

standardSets.append(set_ipa)
#standardSets.append('hi')

activeSets = []

checkboxSetLink_dict = {}

def pickUpExistingSets():
    for set in getSmartSets():
        # Deal with it
        print set.name
        print set.query

class setOrganizer():

    def __init__(self):
        self.w = Window((400,400), 'checkBoxWindow')
        #self.w.checkBox1 = CheckBox((10, 10, -10, -10), 'Label', callback=self.checkBoxCallback, value=True)
        print getSmartSets()

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

        self.w.open()

    def checkBoxCallback(self, sender):
        
        # Get linked set of checkbox
        linkedSetName = checkboxSetLink_dict[sender]
        linkedSet = standardSets_dict[linkedSetName]
        print getSmartSets()

        if sender.get() is 1:
            addSmartSet(linkedSet)
            activeSets.append(linkedSet)
            #print sender.name()
            print 'Aktivieren'
            print getSmartSets()

        else:
            newSmartSetList = []

            print 'activeSets', activeSets
            for set in activeSets:
                if set is linkedSet:
                    print linkedSet, 'entfernt!'
                else:
                    newSmartSetList.append(set)
                    print set, 'noch da'

            setSmartSets(newSmartSetList)
        
        print sender.get(), sender.getTitle()

#pickUpExistingSets()
setOrganizer()