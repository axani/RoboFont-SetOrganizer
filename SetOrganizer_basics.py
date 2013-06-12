from vanilla import *
 
class SetOrganizer:
    
    def __init__(self):
        
        # Basic window
        self.w = Window((400,400), 'SetOrganizer')
        
        # Basic checkbox
        self.w.checkBox1 = CheckBox((10, 10, -10, -10), 'Label', callback=self.checkBoxCallback, value=True)
        self.w.checkBox2 = CheckBox((10, 35, -10, -10), 'Label', callback=self.checkBoxCallback, value=True)
        
        # Open window
        self.w.open()
    
    def checkBoxCallback(self, sender):
        print sender.get(), sender.getTitle()

SetOrganizer()