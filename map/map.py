# Imports

import arcade

# --- Constants ---
CHARACTER_SCALING = 1
TILE_SCALING = 1
TILE_SIZE = 64

class Map() :
	def __init__(self, view) :
		self.view = view
		self.generateMap()

	def generateMap(self) :
		# def offset
		#offset = 4 * self.window.width // 3

		for x in range(0, self.view.game.window.width, 40) :
			for y in range(0, self.view.game.window.width, 40) :
				isox, isoy = self.cart_to_iso(x, y)
				ground = arcade.Sprite("./map/Tiles/Tiles/ts_grass0/straight/225/0.png", TILE_SCALING)
				ground.center_x = isox
				ground.center_y = isoy
				self.view.ground_list.append(ground)

	# Convert cartesian coordinates to isometric
	def cart_to_iso(self, x, y) :
		iso_x = x - y
		iso_y = (x + y) / 2
		return iso_x, iso_y
