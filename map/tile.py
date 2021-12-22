from map.tileSprite import TileSprite

class Tile():
	def __init__(self, blockID, x, y, pointer_to_entity):
		self.blockID = blockID

		self.x=x
		self.y=y
		self.pointer_to_entity = pointer_to_entity

		self.is_locked = 1
		if blockID == "water":
			self.is_locked = 0

		# Sprite
		self.sprite = TileSprite(self)


	def setEntity(self,pointer_to_entity):
		self.is_locked=0
		self.pointer_to_entity=pointer_to_entity
