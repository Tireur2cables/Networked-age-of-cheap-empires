class Personnage:
    def __init__(self, x, y, pt_vie):#constructeur : initialise les attributs
        self.x = x
        self.y = y
        self.pt_vie = pt_vie

    def set_x(self, x):
        self.x = x

    def get_x(self):
        return self.x
    
class Villageois(Personnage):#herite de la classe Personnage
    def __init__(self, x, y):
        Personnage.__init__(self, x, y, 50)#utilise le constructeur de la classe mere
        self.ressource = {"bois" : 0, "nourriture" : 0, "pierre" : 0, "or" : 0}#initialise les attributs specifiques a cette classe

    def nb_ressources(self):
        nb = 0
        for ressource in self.ressource:
            nb += self.ressource[ressource]
        return nb

class Militaire(Personnage):
    def __init__(self, x, y, pt_vie):
        Personnage.__init__(self, x, y, pt_vie)