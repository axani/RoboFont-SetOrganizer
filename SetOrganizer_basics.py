from vanilla import *
from mojo.UI import SmartSet, getSmartSets, setSmartSets

# My standard sets
# ? - Koennte ausgelagert werden

standardSets = []

set_lowercase = SmartSet()
set_lowercase.name = 'Lowercase'
set_lowercase.query = 'Name MATCHES "[a-z]"'

standardSets.append(set_lowercase)
#standardSets.append('hi')

print standardSets


def pickUpExistingSets():
    for set in getSmartSets():
        # Deal with it
        print set.name
        print set.query

class setOrganizer():

    def __init__(self):
        self.w = Window((400,400), 'checkBoxWindow')
        #self.w.checkBox1 = CheckBox((10, 10, -10, -10), 'Label', callback=self.checkBoxCallback, value=True)
        
        # Create a Checkbox for every standard set
        for i in range(len(standardSets)):
            set = standardSets[i]

            checkboxObject = CheckBox((10, 10+30*i, -10, -10), " %s" % set.name, callback=self.checkBoxCallback, value=False)
            setattr(self.w, "checkBox_%s" % i, checkboxObject)

        self.w.open()

    def checkBoxCallback(self, sender):
        print sender.get(), sender.getTitle()

#pickUpExistingSets()
setOrganizer()