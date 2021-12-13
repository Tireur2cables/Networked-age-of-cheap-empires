from map.tileSprite import TileSprite

class Tile():
	def __init__(self, blockID, x, y, pointerToEntity):
		self.blockID = blockID

		self.x=x
		self.y=y
		self.pointerToEntity = pointerToEntity

		self.isLocked = False
		if blockID == "water":
			self.isLocked = True

		# Sprite
		self.sprite = TileSprite(self)


	def setEntity(self,pointerToEntity):
		self.isLocked=True
		self.pointerToEntity=pointerToEntity
