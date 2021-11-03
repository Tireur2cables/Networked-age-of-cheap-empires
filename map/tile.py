
import arcade

# --- Constants ---
CHARACTER_SCALING = 1
TILE_SCALING = 1
TILE_SIZE = 64
TILE_DIST = TILE_SIZE // 2


class Tile():
	def __init__(self, blockID, isLocked, centerCoord, pointerToEntity):
		self.blockID = blockID
		self.isLocked = isLocked
		self.centerCoord = centerCoord
		self.pointerToEntity = pointerToEntity
		self.generateMap()
		
	def generateMap(self):
		# def offset
		# offset = 4 * self.window.width // 3

		for x in range(self.view.game.window.width, 0, -TILE_DIST):
			for y in range(self.view.game.window.width, 0, -TILE_DIST):
				isox, isoy = Map.cart_to_iso(x, y)  # Cette ligne ne recréer pas une map (testé et vérifié).
				ground = arcade.Sprite("./map/Tiles/Tiles/ts_grass0/straight/225/0.png", TILE_SCALING)
				ground.center_x = isox
				ground.center_y = isoy
				self.view.ground_list.append(ground)

	# Convert cartesian coordinates to isometric
	@staticmethod  # This decorator means that the method below won't use information from the instance or the class (we don't use "self").
	def cart_to_iso(x, y):
		iso_x = x - y
		iso_y = (x + y) / 2
		return iso_x, iso_y
