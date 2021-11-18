from arcade import Sprite
from utils.isometric import map_xy_to_iso

# --- Constants ---
TILE_SCALING = 1

class TileSprite(Sprite):
	def __init__(self, id, tile, width, height):
		super().__init__("./map/Tiles/Tiles/ts_grass0/straight/225/0.png", TILE_SCALING)
		self.tile = tile
		tile.sprite = self
		isox, isoy = map_xy_to_iso(tile.x, tile.y, width//2, height//2)  # Cette ligne ne recréer pas une map (testé et vérifié).
		self.center_x = isox
		self.center_y = isoy