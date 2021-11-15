# Imports

import arcade
from map.tile import Tile
# --- Constants ---
CHARACTER_SCALING = 1
TILE_SCALING = 1
MAP_SIZE = 50


class Map():
	def __init__(self, view):
		self.view = view
		self.tileArray= [[Tile(None,False,i,j,None) for i in range(MAP_SIZE)] for j in range(MAP_SIZE)]
		self.generateMap()

	def updateGroundList(self):
		self.view.ground_list.clear()
		for x in range(MAP_SIZE-1,-1, -1):
			for y in range(MAP_SIZE-1,-1, -1):
				self.view.ground_list.append(self.tileArray[x][y].tileSprite)

	# def updateEntityList(self):
	# 	self.view.entity_list.clear()
	# 	for x in range(MAP_SIZE-1,-1, -1):
	# 		for y in range(MAP_SIZE-1,-1, -1):
				
	# 			#self.view.entity_list.append(self.tileArray[x][y].pointerToEntity)

	# def placeAnEntity(self,x,y,pointerToEntity):
	# 	(self.tileArray[x][y]).setEntity(pointerToEntity)
	# 	self.updateEntityList()
		

	# Convert cartesian coordinates to isometric
	@staticmethod  # This decorator means that the method below won't use information from the instance or the class (we don't use "self").
	def cart_to_iso(x, y):
		iso_x = x - y
		iso_y = (x + y) / 2
		return iso_x, iso_y
