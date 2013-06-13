from vanilla import *
from mojo.UI import SmartSet, getSmartSets, setSmartSets, addSmartSet

# My standard sets
# ? - Koennte ausgelagert werden

standardSets = []
standardSets_dict = {}

set_lowercase = SmartSet()
set_lowercase.name = 'Lowercase'
set_lowercase.query = 'Name MATCHES "[a-z]"'

standardSets_dict['set_lowercase'] = set_lowercase

standardSets.append(set_lowercase)
#standardSets.append('hi')

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
            print checkboxSetLink_dict


            i += 1

        self.w.open()

    def checkBoxCallback(self, sender):
        
        # Get linked set of checkbox
        print checkboxSetLink_dict[sender]

        if sender.get() is 1:
            #addSmartSet(self)
            #print sender.name()
            print 'Aktivieren'

        else:
            print 'Deaktivieren'
        
        print sender.get(), sender.getTitle()

#pickUpExistingSets()
setOrganizer()