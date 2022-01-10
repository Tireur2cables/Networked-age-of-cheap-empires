# --- Imports ---
from map.map import Map
from map.map_tests.abstract_perlin_matrix import perlin_array,process_array
from utils.vector import Vector
from entity.Unit import *
from entity.Zone import *
from utils.isometric import *

# -- Constants ---
from CONSTANTS import DEFAULT_MAP_SIZE, TILE_HEIGHT_HALF

# --- Launch setup ---
from LAUNCH_SETUP import LAUNCH_DEFAULT_MAP

#########################################################################
#							MODEL CLASS									#
#########################################################################

class Model():

	def __init__(self, aoce_game):
		""" Initializer """
		self.game = aoce_game

		self.unit_list = []
		self.tile_list = []
		self.zone_list = []

	def setup(self, ressources, ia, isPlayer):
		# clear old lists
		self.unit_list.clear()
		self.tile_list.clear()
		self.zone_list.clear()

		# pre game view infos
		self.isPlayer = isPlayer
		self.default_ressources = ressources
		self.ia = ia
		print(ressources)

		# Set up the villager and add it to the unit_list.
		# self.map = Map(self.tile_list, self.zone_list, DEFAULT_MAP_SIZE)
		use_default = LAUNCH_DEFAULT_MAP
		if use_default:
			self.map = Map(self.tile_list, self.zone_list, DEFAULT_MAP_SIZE)
		else:
			self.map = Map(self.tile_list, self.zone_list, DEFAULT_MAP_SIZE, process_array(perlin_array(seed=69)))

		for pos_spawn in self.map.spawn_array:
			self.add_entity(TownCenter(pos_spawn[0]))
		unit0 = Villager(Vector(100, 100))
		unit1 = Villager(Vector(50, 50))
		unit2 = Villager(grid_pos_to_iso(Vector(3, 2)) + Vector(0, TILE_HEIGHT_HALF))
		self.unit_list.append(unit0)
		self.unit_list.append(unit1)
		self.unit_list.append(unit2)

		#military
		militia = Militia(grid_pos_to_iso(Vector(10, 2)) + Vector(0, TILE_HEIGHT_HALF))
		self.unit_list.append(militia)
		archer = Archer(grid_pos_to_iso(Vector(13, 2)) + Vector(0, TILE_HEIGHT_HALF))
		self.unit_list.append(archer)
		knight = Knight(grid_pos_to_iso(Vector(16, 2)) + Vector(0, TILE_HEIGHT_HALF))
		self.unit_list.append(knight)

	def add_entity(self, new_entity):
		if isinstance(new_entity, Unit) and new_entity not in self.unit_list:
			self.unit_list.append(new_entity)
		elif isinstance(new_entity, Zone) and new_entity not in self.zone_list:
			self.zone_list.append(new_entity)
			self.map.reserve_tile_at(new_entity.grid_position, new_entity.tile_size)

	def discard_entity(self, dead_entity):
		if isinstance(dead_entity, Unit) and dead_entity in self.unit_list:
			self.unit_list.remove(dead_entity)
		elif isinstance(dead_entity, Zone) and dead_entity in self.zone_list:
			self.zone_list.remove(dead_entity)
			self.map.free_tile_at(dead_entity.grid_position, dead_entity.tile_size)
