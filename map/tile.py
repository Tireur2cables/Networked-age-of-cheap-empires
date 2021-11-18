
import arcade
from map.arcadeDisplay import cartToIso

# --- Constants ---
CHARACTER_SCALING = 1
TILE_SCALING = 1
TILE_SIZE = 64
TILE_DIST = TILE_SIZE // 2


class Tile():
	def __init__(self, blockID, isLocked, x, y, pointerToEntity):
		self.blockID = blockID
		self.isLocked = isLocked
		self.x=x*TILE_DIST
		self.y=y*TILE_DIST
		self.pointerToEntity = pointerToEntity


	def setEntity(self,pointerToEntity):
		self.isLocked=True
		self.pointerToEntity=pointerToEntity
