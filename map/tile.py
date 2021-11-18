
import arcade
from map.arcadeDisplay import cartToIso


class Tile():
	def __init__(self, blockID, isLocked, x, y, pointerToEntity):
		self.blockID = blockID
		self.isLocked = isLocked
		self.x=x
		self.y=y
		self.pointerToEntity = pointerToEntity

		# Sprite
		self.sprite = None


	def setEntity(self,pointerToEntity):
		self.isLocked=True
		self.pointerToEntity=pointerToEntity
