# Imports

import arcade
from map.tile import Tile
from entity.Zone import Zone
from map.defaultmap import default_map_2d
# --- Constants ---
CHARACTER_SCALING = 1
TILE_SCALING = 1

class Map():
	def __init__(self, tiles, map_size):
		self.tiles = tiles
		self.map_size = map_size
		# self.tileArray = [[Tile("grass",x,y,None) for y in range(map_size)] for x in range(map_size)]
		self.tileArray = [[Tile(default_map_2d[x][y], x, y, None) for y in range(map_size)] for x in range(map_size)]

# @tidalwaave, 19/12, 23h50 : Time to replace the movements methods, fit 'em in tiles
		self.pathfinding_matrix = [[self.tileArray[x][y].isLocked for y in range(map_size)] for x in range(map_size)]
		

		# for x in range(map_size):
		# 	for y in range(map_size):
		# 		if default_map_2d[x][y] == "tree":
		# 			self.zoneArray = [[Zone(x, y)]]

		self.update_tile_list()

	def update_tile_list(self):
		# self.view.ground_list.clear()  # Do not do this. clear doesn't exist for Arcade.SpriteList().
		for x in range(self.map_size-1,-1, -1):
			for y in range(self.map_size-1,-1, -1):
				self.tiles.append(self.tileArray[x][y])


	def get_tile_at(self, map_position):
		return self.tileArray[map_position.x][map_position.y]
	

####################################################################
#
##
### @tidalwaave : trying to add Zones to map
##
#
	def updateZoneLayer(self):
		pass
