# Imports

from map.tile import Tile
from entity.Zone import Wood, Stone, Gold, BerryBush
from map.defaultmap import default_map_2d, default_map_objects_2d
from utils.isometric import iso_to_grid_pos
from utils.vector import Vector
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

# --- Constants ---
CHARACTER_SCALING = 1

class Map():
	def __init__(self, tiles, objects, map_size, tile_array = None):
		self.tiles = tiles
		self.objects = objects

		self.map_size = map_size
		# self.tile_array = [[Tile("grass",x,y,None) for y in range(map_size)] for x in range(map_size)]
		if tile_array is None:
			self.tile_array = [[Tile(default_map_2d[grid_x][grid_y], Vector(grid_x, grid_y)) for grid_y in range(map_size)] for grid_x in range(map_size)]
		else:
			self.tile_array = tile_array

		self.spawn_array = []

		self.objects_array = [[None for y in range(map_size)] for x in range(map_size)]
		for x in range(map_size):
			for y in range(map_size):
				object = default_map_objects_2d[x][y] if tile_array is None else self.tile_array[x][y].pointer_to_entity
				if tile_array is None:
					self.tile_array[x][y].pointer_to_entity = object

				if object == "tree":  # Can't use match for now, not compatible with arcade library...
					self.objects_array[x][y] = Wood(Vector(x, y))
				elif object == "stone":
					self.objects_array[x][y] = Stone(Vector(x, y))
				elif object == "gold":
					self.objects_array[x][y] = Gold(Vector(x, y))
				elif object == "berry":
					self.objects_array[x][y] = BerryBush(Vector(x, y))
				elif object is not None and "spawn" in object:
					self.spawn_array.append((Vector(x, y), int(object.split("_")[1])))
				if self.objects_array[x][y] and self.objects_array[x][y].is_locking:
					self.tile_array[x][y].is_free = 0

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
		return [[self.tile_array[x][y].is_free for x in range(self.map_size)] for y in range(self.map_size)]

	def get_path(self, start, end):
		# Pathfinding algorithm
		pathfinding_matrix = self.get_pathfinding_matrix()
		grid = Grid(matrix=pathfinding_matrix)
		finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
		start = grid.node(*start)
		end = grid.node(*end)
		path, runs = finder.find_path(start, end, grid)
		return path

	def get_tile_at(self, map_position):
		return self.tile_array[map_position.x][map_position.y]

	def get_tiles_nearby(self, map_position):
		return tuple(self.tile_array[map_position.x + i][map_position.y + j] for i in range(-1, 2) for j in range(-1, 2))

	def free_tile_at(self, map_position, tile_size):
		for x in range(map_position.x, map_position.x + tile_size[0]):
			for y in range(map_position.y, map_position.y + tile_size[1]):
				if self.objects_array[x][y] is not None or self.tile_array[x][y].pointer_to_entity is not None:
					self.objects_array[x][y] = None
					self.tile_array[x][y].pointer_to_entity = None
				self.tile_array[x][y].is_free = 1

	def reserve_tile_at(self, map_position, tile_size):
		for x in range(map_position.x, map_position.x + tile_size[0]):
			for y in range(map_position.y, map_position.y + tile_size[1]):
				self.tile_array[x][y].is_free = 0

####################################################################
#
##
### @tidalwaave : trying to add Zones to map
##
#
	def updateZoneLayer(self):
		pass
