from entity.Entity import Entity
from utils.SpriteData import SpriteData
from CONSTANTS import Resource as Res
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
	#Liste des Unit: https://ageofempires.fandom.com/wiki/Units_(Age_of_Empires_II)
	def __init__(self, iso_position, speed=5, **kwargs):
		super().__init__(iso_position, **kwargs)

		# Movement
		self.aim = Vector(0, 0)  # coordinate aimed by the user when he clicked
		self.aimed_entity = None
		self.path = []
		self.change = Vector(0, 0)  # The change of coordinate calculated from the speed. This may be moved in the Controller in the future.
		self.speed = speed  # Speed of the unit
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
	creation_cost = {Res.FOOD : 50, Res.WOOD : 0, Res.GOLD : 0, Res.STONE : 0}
	creation_time = 25
	def __init__(self, iso_position):
		super().__init__(iso_position, sprite_data=SpriteData("Ressources/img/units/villager_stand.png", y_offset=46//2), speed=0.8, health=25, damage=3, rate_fire=2, line_sight=4)
		self.resource = {Res.FOOD : 0, Res.WOOD : 0, Res.GOLD : 0, Res.STONE : 0} # utilisation de l'enumeration Resource
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

#Infantry (Trained at Barracks)
class Militia(Military):
	creation_cost = {Res.FOOD : 60, Res.WOOD : 0, Res.GOLD : 20, Res.STONE : 0}
	creation_time = 21
	def __init__(self, iso_position):
		super().__init__(iso_position, sprite_data=SpriteData("Ressources/img/units/militia_stand.png"), speed = 0.9, health=40, damage=4, rate_fire=2, pierce_armor=1, line_sight=4)

class Spearman(Military):
	creation_cost = {Res.FOOD : 35, Res.WOOD : 25, Res.GOLD : 0, Res.STONE : 0}
	creation_time = 22
	def __init__(self, iso_position):
		super().__init__(iso_position, sprite_data=SpriteData("Ressources/img/units/spearman_stand.png"), speed=1, health=45, damage=3, rate_fire=3, line_sight=4)

#Archery (Trained at Archery Range)
#For the moment, all archery units deal instant damage (there is no projectile) and they aim parfectly well.
class Archer(Military):
	creation_cost = {Res.FOOD : 0, Res.WOOD : 25, Res.GOLD : 45, Res.STONE : 0}
	creation_time = 35
	def __init__(self, iso_position):
		super().__init__(iso_position, sprite_data=SpriteData("Ressources/img/units/archer_stand.png"), speed=0.96, health=30, damage=4, rate_fire=2, range=4, line_sight=6)

class Skirmisher(Military):
	creation_cost = {Res.FOOD : 25, Res.WOOD : 35, Res.GOLD : 0, Res.STONE : 0}
	creation_time = 22
	def __init__(self, iso_position):
		super().__init__(iso_position, sprite_data=SpriteData("Ressources/img/units/skirmisher_stand.png"), speed=0.96, health=30, damage=2, rate_fire=3, range=4, pierce_armor=3, line_sight=6)

#Cavalry (Trained at Stable)
class ScoutCavalry(Military):
	creation_cost = {Res.FOOD : 80, Res.WOOD : 0, Res.GOLD : 0, Res.STONE : 0}
	creation_time = 30
	def __init__(self, iso_position):
		super().__init__(iso_position, sprite_data=SpriteData("Ressources/img/units/scoutcavalry_stand.png"), speed=1.2, health=45, damage=3, rate_fire=2, pierce_armor=2, line_sight=4)

class Knight(Military):
	creation_cost = {Res.FOOD : 60, Res.WOOD : 0, Res.GOLD : 75, Res.STONE : 0}
	creation_time = 30
	def __init__(self, iso_position):
		super().__init__(iso_position, sprite_data=SpriteData("Ressources/img/units/knight_stand.png"), speed=1.35, health=100, damage=10, rate_fire=1.8, melee_armor=2, pierce_armor=2, line_sight=4)
