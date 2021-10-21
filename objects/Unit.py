from objects.Entity import Entity
from CONSTANTS import Resource
from utils.vector import Vector


class Unit(Entity):
	#une Unit est une Entity qui est mobile
	#Liste des Unit: https://ageofempires.fandom.com/wiki/Units_(Age_of_Empires)
	def __init__(self, position, health, damage, display=None, rate_fire=1, range=0, melee_armor=0, pierce_armor=0, line_sight=4, speed=5):
		super().__init__(position, health, damage, display, rate_fire=rate_fire, range=range, melee_armor=melee_armor, pierce_armor=pierce_armor, line_sight=line_sight)

		# Movement
		self.aim = Vector(0, 0)  # coordinate aimed by the user when he clicked
		self.change = Vector(0, 0)  # The change of coordinate calculated from the speed. This may be moved in the Controller in the future.
		self.speed = speed  # Speed of the villager (should probably be a constant)

	# Function for movement, may change in the future when pathfinding will be needed.
	def aim_towards(self, aim, change):
		self.aim = aim
		self.change = change



class Villager(Unit):#un Villageois est une Unit particuliere
	def __init__(self, position, health=25, damage=3, display = None, rate_fire=1.5, range=0, melee_armor=0, pierce_armor=0, line_sight=4, speed=1):
		super().__init__(position, health, damage, display, rate_fire=rate_fire, range=range, melee_armor=melee_armor, pierce_armor=pierce_armor, line_sight=line_sight, speed=speed)
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
	def __init__(self, position, health, damage, rate_fire=1, range=0, melee_armor=0, pierce_armor=0, line_sight=4, speed=1):
		super().__init__(position, health, damage, rate_fire=rate_fire, range=range, melee_armor=melee_armor, pierce_armor=pierce_armor, line_sight=line_sight, speed=speed)

# Rq : Il n'est peut-être pas utile de creer les implementation de chaque type de militaire car cela n'apporte pas vraiment d'interet
"""
#Infantry
class Clubman(Military):
	def __init__(self, position, health=40, damage=3):
		super().__init__(position, health, damage)

class Swordsman(Military):
	def __init__(self, position, health=60, damage=7):
		super().__init__(position, health, damage)

#Archery
class Bowman(Military):
	def __init__(self, position, health=35, damage=3):
		super().__init__(position, health, damage)

class ImprovedBowman(Military):
	def __init__(self, position, health=40, damage=4):
		super().__init__(position, health, damage)

#Cavalry
class Scout(Military):
	def __init__(self, position, health=60, damage=3):
		super().__init__(position, health, damage)

class Cavalry(Military):
	def __init__(self, position, health=150, damage=8):
		super().__init__(position, health, damage)
"""
