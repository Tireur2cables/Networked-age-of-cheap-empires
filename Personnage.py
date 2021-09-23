class Personnage:
    def __init__(self, x, y, pt_vie, degats):#constructeur : initialise les attributs
        self.x = x
        self.y = y
        self.pt_vie = pt_vie
        self.max_pt_vie = pt_vie
        self.degats = degats

    #coordonnees
    def set_x(self, x):
        self.x = x

    def get_x(self):
        return self.x
    
    def set_y(self, y):
        self.y = y

    def get_y(self):
        return self.y

    #combats
    def get_pt_vie(self):
        return self.pt_vie
    
    def get_max_pt_vie(self):
        return self.max_pt_vie

    def set_max_pt_vie(self, max_pt_vie):
        self.max_pt_vie = max_pt_vie

    def est_en_vie(self):
        return self.pt_vie > 0
    
    def gagne_pt_vie(self, qte_pt_vie):
        self.pt_vie += qte_pt_vie
        if self.pt_vie > self.max_pt_vie:#on corrige le nb de pt de vie si celui-ci est superieur au maximum
            self.pt_vie = self.max_pt_vie
    
    def perd_pt_vie(self, qte_pt_vie):
        self.pt_vie -= qte_pt_vie
        if self.pt_vie < 0:#on corrige le nb de pt de vie si celui-ci est negatif
            self.pt_vie = 0

    def get_degats(self):
        return self.degats
    
    def set_degats(self, degats):
        self.degats = degats
    
class Villageois(Personnage):#herite de la classe Personnage
    def __init__(self, x, y):
        super().__init__(self, x, y, 50, 3)#utilise le constructeur de la classe mere
        self.ressource = {"bois" : 0, "nourriture" : 0, "pierre" : 0, "or" : 0}#initialise les attributs specifiques a cette classe
        self.max_ressource = 10

    def nb_ressources(self):
        nb = 0
        for ressource in self.ressource:
            nb += self.ressource[ressource]
        return nb
    
    def est_plein(self):#ne peut plus prendre de nouvelles ressources
        return self.nb_ressources() == self.max_ressource

class Militaire(Personnage):
    def __init__(self, x, y, pt_vie, degats):
        super().__init__(self, x, y, pt_vie, degats)
