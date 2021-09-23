class Zone:
    def __init__(self, x, y):#constructeur : initialise les attributs
        self.x = x
        self.y = y
        #self.health = health
# Zone : Base brick of something that is present on the map, and not IN the map
#        Has a position, appears and disappears from the map
#   
# 
# Subclasses of Zone : 
# Buildable : Civil, Military, Economic (no subclass & no need to differenciate)
# Resources (Natural !) : Mines, trees, 

#FILE NAMING CONVENTION : Zone_Buildable_TownCenter.py IN SUBFOLDERS ????


    
class Buildable(Zone):#Inherits from Zone class, thus has coordinates; Will have area when implemented on map
    def __init__(self, x, y, health):
        super().__init__(self, x, y)#Calls parent class constructor
        self.health = health





