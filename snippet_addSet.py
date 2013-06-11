# RoboFont-SetOrganizer - Snippet
# Add set

from mojo.UI import SmartSet, addSmartSet

newSet = SmartSet()
newSet.name = 'New Set'
newSet.query = 'Name MATCHES "[a-z]"'

addSmartSet(newSet)