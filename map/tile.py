from map.tileSprite import TileSprite
from utils.SpriteData import SpriteData
from utils.vector import Vector

class Tile():
	def __init__(self, blockID, grid_position, pointer_to_entity=None):
		self.blockID = blockID

		self.grid_position=grid_position
		self.pointer_to_entity = pointer_to_entity  # For now, pointer_to_entity is never used.

		self.is_free = 1
		if blockID == "water":
			self.is_free = 0

		# Sprite
		#self.init_sprite()

	def __getstate__(self):
		return [self.blockID, self.grid_position, self.is_free]

	def __setstate__(self, data):
		self.blockID = data[0]
		self.grid_position = data[1]
		self.is_free = data[2]
		#self.pointer_to_entity = data[3]
		self.init_sprite()

	def init_sprite(self):
		sprite_data = SpriteData(file="./Ressources/img/tiles/" + self.blockID + ".png", y_offset=16)
		self.sprite = TileSprite(self, sprite_data)

	def setEntity(self,pointer_to_entity):
		self.pointer_to_entity=pointer_to_entity
		if pointer_to_entity.is_locking:
			self.is_free = 0
		else:
			self.is_free = 1
