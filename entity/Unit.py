from entity.Entity import Entity
from CONSTANTS import Resource
from utils.vector import Vector


#   _    _           _   _
#  | |  | |         (_) | |
#  | |  | |  _ __    _  | |_
#  | |  | | | '_ \  | | | __|
#  | |__| | | | | | | | | |_
#   \____/  |_| |_| |_|  \__|




class Unit(Entity):
	#une Unit est une Entity qui est mobile
	#Liste des Unit: https://ageofempires.fandom.com/wiki/Units_(Age_of_Empires)
	def __init__(self, position, speed=5, **kwargs):
		super().__init__(position, **kwargs)

		# Movement
		self.aim = Vector(0, 0)  # coordinate aimed by the user when he clicked
		self.change = Vector(0, 0)  # The change of coordinate calculated from the speed. This may be moved in the Controller in the future.
		self.speed = speed  # Speed of the villager (should probably be a constant)

	# Function for movement, may change in the future when pathfinding will be needed.
	def aim_towards(self, aim, change):
		self.aim = aim
		self.change = change


#  __      ___ _ _
#  \ \    / (_) | |
#   \ \  / / _| | | __ _  __ _  ___ _ __
#    \ \/ / | | | |/ _` |/ _` |/ _ \ '__|
#     \  /  | | | | (_| | (_| |  __/ |
#      \/   |_|_|_|\__,_|\__, |\___|_|
#                         __/ |
#                        |___/


class Villager(Unit):#un Villageois est une Unit particuliere
	def __init__(self, position):
		super().__init__(position, sprite_image="Movements/coin_01.png", health=25, damage=3, rate_fire=1.5)
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


#   __  __ _ _ _ _
#  |  \/  (_) (_) |
#  | \  / |_| |_| |_ __ _ _ __ _   _
#  | |\/| | | | | __/ _` | '__| | | |
#  | |  | | | | | || (_| | |  | |_| |
#  |_|  |_|_|_|_|\__\__,_|_|   \__, |
#                               __/ |
#                              |___/


class Military(Unit):#un Militaire est une Unit particuliere
	def __init__(self, position, **kwargs):
		super().__init__(position, **kwargs)

# Rq : Il n'est peut-être pas utile de creer les implementation de chaque type de militaire car cela n'apporte pas vraiment d'interet

#Infantry
class Clubman(Military):
	def __init__(self, position):
		super().__init__(position, sprite_image="Movements/coin_01.png", health=40, damage=3)

class Swordsman(Military):
	def __init__(self, position):
		super().__init__(position, sprite_image="Movements/coin_01.png", health=60, damage=7)

#Archery
class Bowman(Military):
	def __init__(self, position):
		super().__init__(position, sprite_image="Movements/coin_01.png", health=35, damage=3)

class ImprovedBowman(Military):
	def __init__(self, position):
		super().__init__(position, sprite_image="Movements/coin_01.png", health=40, damage=4)

#Cavalry
class Scout(Military):
	def __init__(self, position):
		super().__init__(position, sprite_image="Movements/coin_01.png", health=60, damage=3)

class Cavalry(Military):
	def __init__(self, position):
		super().__init__(position, sprite_image="Movements/coin_01.png", health=150, damage=8)
