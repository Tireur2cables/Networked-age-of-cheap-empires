from arcade import Sprite
from utils.isometric import map_xy_to_iso

# --- Constants ---
TILE_SCALING = 1

class TileSprite(Sprite):
	def __init__(self, id, tile, width, height):
		self.tile = tile
		tile.sprite = self
		super().__init__("./map/Tiles/" + self.tile.blockID + ".png", TILE_SCALING)

		isox, isoy = map_xy_to_iso(tile.x, tile.y, width//2, height//2)  # Cette ligne ne recréer pas une map (testé et vérifié).
		self.center_x = isox
		self.center_y = isoy