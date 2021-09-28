from Entity import *

class Unit(Entity):
    #une Unit est une Entity qui est mobile
    #Liste des Unit: https://ageofempires.fandom.com/wiki/Units_(Age_of_Empires) 
    def __init__(self, x, y, health, damage, rate_fire=1, range=0, melee_armor=0, pierce_armor=0, line_sight=4, speed=1):
        super().__init__(x, y, health, damage, rate_fire=rate_fire, range=range, melee_armor=melee_armor, pierce_armor=pierce_armor, line_sight=line_sight)
        self.speed = speed

class Villager(Unit):#un Villageois est une Unit particuliere
    def __init__(self, x, y, health=25, damage=3, rate_fire=1.5, range=0, melee_armor=0, pierce_armor=0, line_sight=4, speed=1):
        super().__init__(x, y, health, damage, rate_fire=rate_fire, range=range, melee_armor=melee_armor, pierce_armor=pierce_armor, line_sight=line_sight, speed=speed)
        self.resource = {Resource.FOOD : 0, Resource.WOOD : 0, Resource.STONE : 0, Resource.GOLD : 0}#utilisation de l'enumeration Resource
        self.max_resource = 10

    def nb_resources(self):
        nb = 0
        for resource in self.resource:
            nb += self.resource[resource]
        return nb
    
    def set_max_resource(self, max_resource):
        self.max_resource = max_resource

    def is_full(self):#ne peut plus prendre de nouvelles resources
        return self.nb_resources() == self.max_resource

class Military(Unit):#un Militaire est une Unit particuliere
    def __init__(self, x, y, health, damage, rate_fire=1, range=0, melee_armor=0, pierce_armor=0, line_sight=4, speed=1):
        super().__init__(x, y, health, damage, rate_fire=rate_fire, range=range, melee_armor=melee_armor, pierce_armor=pierce_armor, line_sight=line_sight, speed=speed)

# Rq : Il n'est peut-être pas utile de creer les implementation de chaque type de militaire car cela n'apporte pas vraiment d'interet
"""
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
"""
