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

	def setup(self, ressources, players):
		# clear old lists
		self.unit_list.clear()
		self.tile_list.clear()
		self.zone_list.clear()

		# pre game view infos
		self.players = players
		self.default_ressources = ressources
		print(ressources)

		# Set up the villager and add it to the unit_list.
		# self.map = Map(self.tile_list, self.zone_list, DEFAULT_MAP_SIZE)
		use_default = LAUNCH_DEFAULT_MAP
		if use_default:
			self.map = Map(self.tile_list, self.zone_list, DEFAULT_MAP_SIZE)
		else:
			self.map = Map(self.tile_list, self.zone_list, DEFAULT_MAP_SIZE, process_array(perlin_array(seed=69)))

		for pos_spawn in self.map.spawn_array:
			faction = "player" if pos_spawn[1] == "0" else "ai_" + pos_spawn[1]
			self.game.game_controller.add_entity_to_game(TownCenter(pos_spawn[0], faction))

			start_villagers = (Villager(grid_pos_to_iso(pos_spawn[0] - Vector(1, 1)), faction),
				Villager(grid_pos_to_iso(pos_spawn[0] - Vector(0, 1)), faction),
				Villager(grid_pos_to_iso(pos_spawn[0] - Vector(1, 0)), faction))

			for v in start_villagers:
				self.game.game_controller.add_entity_to_game(v)

		# units = (Villager(Vector(100, 100), "player"),
		# Villager(Vector(50, 50), "player"),
		# Villager(grid_pos_to_iso(Vector(3, 2)) + Vector(0, TILE_HEIGHT_HALF),"player"))
		# for unit in units:
		# 	self.game.game_controller.add_entity_to_game(unit)

		# #military
		# militaries = (Militia(grid_pos_to_iso(Vector(10, 2)) + Vector(0, TILE_HEIGHT_HALF), "player"),
		# Archer(grid_pos_to_iso(Vector(13, 2)) + Vector(0, TILE_HEIGHT_HALF), "player"),
		# Knight(grid_pos_to_iso(Vector(16, 2)) + Vector(0, TILE_HEIGHT_HALF), "player")
		# )

		# for military in militaries:
		# 	self.game.game_controller.add_entity_to_game(military)

	def add_entity(self, new_entity):
		if isinstance(new_entity, Unit) and new_entity not in self.unit_list:
			self.unit_list.append(new_entity)
		elif isinstance(new_entity, Zone) and new_entity not in self.zone_list:
			self.zone_list.append(new_entity)
			self.map.add_entity_to_pos(new_entity)
			self.map.reserve_tile_at(new_entity.grid_position, new_entity.tile_size)

	def discard_entity(self, dead_entity):
		if isinstance(dead_entity, Unit) and dead_entity in self.unit_list:
			self.unit_list.remove(dead_entity)
		elif isinstance(dead_entity, Zone) and dead_entity in self.zone_list:
			self.zone_list.remove(dead_entity)
			self.map.free_tile_at(dead_entity.grid_position, dead_entity.tile_size)