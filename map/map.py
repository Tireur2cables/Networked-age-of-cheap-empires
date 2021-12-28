# Imports

import arcade
from arcade.arcade_types import PointList
from map.tile import Tile
from entity.Zone import Wood, Stone, Gold
from map.defaultmap import default_map_2d, default_map_objects_2d
from utils.vector import Vector

# --- Constants ---
CHARACTER_SCALING = 1

class Map():
	def __init__(self, tile_array, tiles, objects, map_size):
		# self.tiles = tiles
		# self.objects = objects
		self.tile_array = tile_array

		self.map_size = map_size
		# self.tile_array = [[Tile("grass",x,y,None) for y in range(map_size)] for x in range(map_size)]
		if not(self.tile_array):
			self.tile_array = [[Tile(default_map_2d[grid_x][grid_y], grid_x, grid_y) for grid_y in range(map_size)] for grid_x in range(map_size)]

		self.objects_array = [[None for y in range(map_size)] for x in range(map_size)]
		for x in range(map_size):
			for y in range(map_size):
				object = default_map_objects_2d[x][y]
				if object == "tree":  # Can't use match for now, not compatible with arcade library...
					self.objects_array[x][y] = Wood(Vector(x, y))
				elif object == "stone":
					self.objects_array[x][y] = Stone(Vector(x, y))
				elif object == "gold":
					self.objects_array[x][y] = Gold(Vector(x, y))
				if self.objects_array[x][y] and self.objects_array[x][y].is_locking:
					self.tile_array[x][y].is_locked = 0

		self.update_tile_list()

	def update_tile_list(self):
		# self.view.ground_list.clear()  # Do not do this. clear doesn't exist for Arcade.SpriteList().
		for x in range(self.map_size-1,-1, -1):
			for y in range(self.map_size-1,-1, -1):
				self.tiles.append(self.tile_array[x][y])
				if self.objects_array[x][y]:
					self.objects.append(self.objects_array[x][y])

	def get_pathfinding_matrix(self):  # @kenzo6c: The pathfinding_matrix has to be created on the fly, otherwise it won't change if the map changes
		# @tidalwaave, 19/12, 23h50 : Time to replace the movements methods, fit 'em in tiles
		# Swapping x and y here, because of the library implementation
		return [[self.tile_array[x][y].is_locked for x in range(self.map_size)] for y in range(self.map_size)]


	def get_tile_at(self, map_position):
		return self.tile_array[map_position.x][map_position.y]


####################################################################
#
##
### @tidalwaave : trying to add Zones to map
##
#
	def updateZoneLayer(self):
		pass
