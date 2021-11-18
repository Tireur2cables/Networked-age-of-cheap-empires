from arcade import Sprite

TILE_SCALING = 1

class TileSprite(Sprite):
	def __init__(self, id, tile):
		super().__init__("./map/Tiles/Tiles/ts_grass0/straight/225/0.png", TILE_SCALING)
		isox, isoy = TileSprite.cart_to_iso(tile.x, tile.y)  # Cette ligne ne recréer pas une map (testé et vérifié).
		self.center_x = isox
		self.center_y = isoy

	@staticmethod  # This decorator means that the method below won't use information from the instance or the class (we don't use "self").
	def cart_to_iso(x, y):
		iso_x = x - y
		iso_y = (x + y) / 2
		return iso_x, iso_y