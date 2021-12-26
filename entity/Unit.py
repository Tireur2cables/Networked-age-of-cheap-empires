from entity.Entity import Entity
from utils.SpriteData import SpriteData
from CONSTANTS import Resource
from utils.vector import Vector
from utils.isometric import *
# Pathfinding / movement imports
# TODO : pip3 install pathfinding
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder


#   _    _           _   _
#  | |  | |         (_) | |
#  | |  | |  _ __    _  | |_
#  | |  | | | '_ \  | | | __|
#  | |__| | | | | | | | | |_
#   \____/  |_| |_| |_|  \__|


class Unit(Entity):
	#une Unit est une Entity qui est mobile
	#Liste des Unit: https://ageofempires.fandom.com/wiki/Units_(Age_of_Empires)
	def __init__(self, iso_position, speed=5, **kwargs):
		super().__init__(iso_position, **kwargs)

		# Movement
		self.aim = Vector(0, 0)  # coordinate aimed by the user when he clicked
		self.aimed_entity = None
		self.path = []
		self.change = Vector(0, 0)  # The change of coordinate calculated from the speed. This may be moved in the Controller in the future.
		self.speed = speed  # Speed of the villager (should probably be a constant)
		self.is_moving = False

	def set_path(self, path):
		self.path = path
		self.is_moving = True

	# Function for movement, may change in the future when pathfinding will be needed.
	def next_aim(self):
		self.aim = grid_pos_to_iso(Vector(*self.path.pop(0)))
		# The following calculation is necessary to have uniform speeds :
		self.change = self.speed * ((self.aim - self.iso_position).normalized())
		# We want the same speed no matter what the distance between the villager and where he needs to go is.





#  __      ___ _ _
#  \ \    / (_) | |
#   \ \  / / _| | | __ _  __ _  ___ _ __
#    \ \/ / | | | |/ _` |/ _` |/ _ \ '__|
#     \  /  | | | | (_| | (_| |  __/ |
#      \/   |_|_|_|\__,_|\__, |\___|_|
#                         __/ |
#                        |___/


class Villager(Unit):#un Villageois est une Unit particuliere
	def __init__(self, iso_position):
		super().__init__(iso_position, sprite_data=SpriteData("Ressources/img/units/villager_stand.png", y_offset=46//2), health=25, damage=3, rate_fire=1.5)
		self.resources = {"food" : 0, "wood" : 0, "stone" : 0, "gold" : 0} # utilisation de l'enumeration Resource --- Annulé pour l'instant
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
	def __init__(self, iso_position, **kwargs):
		super().__init__(iso_position, **kwargs)

# Rq : Il n'est peut-être pas utile de creer les implementation de chaque type de militaire car cela n'apporte pas vraiment d'interet

#Infantry
class Clubman(Military):
	def __init__(self, iso_position):
		super().__init__(iso_position, sprite_data=SpriteData("Movements/coin_01.png"), health=40, damage=3)

class Swordsman(Military):
	def __init__(self, iso_position):
		super().__init__(iso_position, sprite_data=SpriteData("Movements/coin_01.png"), health=60, damage=7)

#Archery
class Bowman(Military):
	def __init__(self, iso_position):
		super().__init__(iso_position, sprite_data=SpriteData("Movements/coin_01.png"), health=35, damage=3)

class ImprovedBowman(Military):
	def __init__(self, iso_position):
		super().__init__(iso_position, sprite_data=SpriteData("Movements/coin_01.png"), health=40, damage=4)

#Cavalry
class Scout(Military):
	def __init__(self, iso_position):
		super().__init__(iso_position, sprite_data=SpriteData("Movements/coin_01.png"), health=60, damage=3)

class Cavalry(Military):
	def __init__(self, iso_position):
		super().__init__(iso_position, sprite_data=SpriteData("Movements/coin_01.png"), health=150, damage=8)
