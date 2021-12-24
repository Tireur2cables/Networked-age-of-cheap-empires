from map.tileSprite import TileSprite
from utils.SpriteData import SpriteData

class Tile():
	def __init__(self, blockID, grid_x, grid_y, pointer_to_entity):
		self.blockID = blockID

		self.grid_x=grid_x
		self.grid_y=grid_y
		self.pointer_to_entity = pointer_to_entity

		self.is_locked = 1
		if blockID == "water":
			self.is_locked = 0

		# Sprite
		sprite_data = SpriteData(file="./map/Tiles/" + self.blockID + ".png", y_offset=16)
		self.sprite = TileSprite(self, sprite_data)


	def setEntity(self,pointer_to_entity):
		self.is_locked=0
		self.pointer_to_entity=pointer_to_entity
