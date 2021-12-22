from map.tileSprite import TileSprite

class Tile():
	def __init__(self, blockID, x, y, pointerToEntity):
		self.blockID = blockID

		self.x=x
		self.y=y
		self.pointerToEntity = pointerToEntity

		self.isLocked = 1
		if blockID == "water":
			self.isLocked = 0

		# Sprite
		self.sprite = TileSprite(self)


	def setEntity(self,pointerToEntity):
		self.isLocked=0
		self.pointerToEntity=pointerToEntity
