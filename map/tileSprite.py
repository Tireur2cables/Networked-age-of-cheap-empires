from arcade import Sprite
from utils.isometric import grid_xy_to_iso

class TileSprite(Sprite):
	def __init__(self, tile, sprite_data):
		super().__init__(filename=sprite_data.file, scale=sprite_data.scale)

		self.tile = tile

		isox, isoy = grid_xy_to_iso(tile.grid_x, tile.grid_y)  # Cette ligne ne recréer pas une map (testé et vérifié).
		self.center_x = isox + sprite_data.x_offset
		self.center_y = isoy + sprite_data.y_offset