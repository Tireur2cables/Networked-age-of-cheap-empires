class Zone:
    def __init__(self, x, y):#constructeur : initialise les attributs
        self.x = x
        self.y = y
        
# Getting and setting coordinates from the building
    def set_x(self, x):
        self.x = x

    def get_x(self):
        return self.x

    def set_y(self, y):
        self.y = y

    def get_y(self):
        return self.y
# Zone : Base brick of something that is present on the map, and not IN the map
#        Has a position, appears and disappears from the map
#   
# 
# Subclasses of Zone : 
# Buildable : Civil, Military, Economic (no subclass & no need to differenciate)
# Resources (Natural !) : Mines, trees, 
# Between both : buildable resources (champs)

# Tasklist : 
# Town Center 
# Buisson cueillette 





#FILE NAMING CONVENTION : Zone_Buildable_TownCenter.py IN SUBFOLDERS ????


    
class Buildable(Zone):#Inherits from Zone class, thus has coordinates; Will have area when implemented on map
    def __init__(self, x, y, health):
        super().__init__(self, x, y) # Calls parent class constructor
        self.health = health
        self.maxhealth = health


    def set_health(self, health):
        self.health = health
    def get_health(self):
        return self.health
    
    def set_maxhealth(self):
        return self.maxhealth
    def get_maxhealth(self):
        return self.maxhealth

# intégrer préconditions de construction de bat dans bat qui permet de construire bat
# avancées tech : fonction boucle faisant appel aux fonctions des objets respectifs pour modif leur propriétés

class TownCenter(Buildable):#Inherits from Zone class, thus has coordinates; Will have area when implemented on map
    def __init__(self, x, y, health = 600):
        super().__init__(self, x, y, health)

    def get_health(self):
        return self.health
    





