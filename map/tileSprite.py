from arcade import Sprite
from utils.isometric import grid_xy_to_iso

# --- Constants ---
TILE_SCALING = 1
TILE_WIDTH = 64
TILE_HEIGHT = TILE_WIDTH // 2

class TileSprite(Sprite):
	def __init__(self, tile):
		self.tile = tile
		super().__init__("./map/Tiles/" + self.tile.blockID + ".png", TILE_SCALING)

		isox, isoy = grid_xy_to_iso(tile.grid_x, tile.grid_y, TILE_WIDTH//2, TILE_HEIGHT//2)  # Cette ligne ne recréer pas une map (testé et vérifié).
		self.center_x = isox
		self.center_y = isoy