from Entity import *

class Unit(Entity):
    #une unite est une Entity qui est mobile
    #Liste des Unit: https://ageofempires.fandom.com/wiki/Units_(Age_of_Empires) 
    def __init__(self, x, y, health, damage):
        super().__init__(x, y, health, damage)

class Villager(Unit):#un Villageois est une Unit particuliere
    def __init__(self, x, y, health=25, damage=3):
        super().__init__(x, y, health, damage)#utilise le constructeur de la classe mere
        #!!!!!!!! Faire une enumeration pour le nom des ressources
        #avec un acces en faisant Resource.WOOD, Resource.FOOD ...
        self.resource = {"bois" : 0, "nourriture" : 0, "pierre" : 0, "or" : 0}#initialise les attributs specifiques a cette classe
        self.max_resource = 10

    def nb_resources(self):
        nb = 0
        for resource in self.resource:
            nb += self.resource[resource]
        return nb
    
    def is_full(self):#ne peut plus prendre de nouvelles resources
        return self.nb_resources() == self.max_resource

class Military(Unit):#un Militaire est une Unit particuliere
    def __init__(self, x, y, health, damage):
        super().__init__(self, x, y, health, damage)

#Infantry
class Clubman(Military):
    def __init__(self, x, y, health=40, damage=3):
        super().__init__(x, y, health, damage)

class Swordsman(Military):
    def __init__(self, x, y, health=60, damage=7):
        super().__init__(x, y, health, damage)

#Archery
class Bowman(Military):
    def __init__(self, x, y, health=35, damage=3):
        super().__init__(x, y, health, damage)

class ImprovedBowman(Military):
    def __init__(self, x, y, health=40, damage=4):
        super().__init__(x, y, health, damage)

#Cavalry
class Scout(Military):
    def __init__(self, x, y, health=60, damage=3):
        super().__init__(x, y, health, damage)

class Cavalry(Military):
    def __init__(self, x, y, health=150, damage=8):
        super().__init__(x, y, health, damage)
