# Imports

import arcade
from map.tile import Tile
# --- Constants ---
CHARACTER_SCALING = 1
TILE_SCALING = 1

class Map():
	def __init__(self, view, map_size):
		self.view = view
		self.map_size = map_size
		self.tileArray= [[Tile("grass",x,y,None) for y in range(map_size)] for x in range(map_size)]
		self.updateGroundList()

	def updateGroundList(self):
		# self.view.ground_list.clear()  # Do not do this. clear doesn't exist for Arcade.SpriteList().
		for x in range(self.map_size-1,-1, -1):
			for y in range(self.map_size-1,-1, -1):
				self.view.ground_list.append(self.tileArray[x][y])

	def get_tile_at(self, map_position):
		return self.tileArray[map_position.x][map_position.y]


	# def updateEntityList(self):
	# 	self.view.entity_list.clear()
	# 	for x in range(self.map_size-1,-1, -1):
	# 		for y in range(self.map_size-1,-1, -1):

	# 			#self.view.entity_list.append(self.tileArray[x][y].pointerToEntity)

	# def placeAnEntity(self,x,y,pointerToEntity):
	# 	(self.tileArray[x][y]).setEntity(pointerToEntity)
	# 	self.updateEntityList()
