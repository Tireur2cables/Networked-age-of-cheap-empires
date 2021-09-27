from Entity import *
    
class Villager(Unit):#herite de la classe Personnage
    def __init__(self, x, y):
        super().__init__(self, x, y, 50, 3)#utilise le constructeur de la classe mere
        self.ressource = {"bois" : 0, "nourriture" : 0, "pierre" : 0, "or" : 0}#initialise les attributs specifiques a cette classe
        self.max_ressource = 10

    def nb_ressources(self):
        nb = 0
        for ressource in self.ressource:
            nb += self.ressource[ressource]
        return nb
    
    def is_full(self):#ne peut plus prendre de nouvelles ressources
        return self.nb_ressources() == self.max_ressource

class Military(Unit):
    def __init__(self, x, y, health, damage):
        super().__init__(self, x, y, health, damage)


