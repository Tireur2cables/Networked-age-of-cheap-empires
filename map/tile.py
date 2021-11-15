
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
		self.tileSprite=self.generateSprite(self.x,self.y)
		

	def generateSprite(self, x, y):
		isox, isoy = Tile.cart_to_iso(x, y)  # Cette ligne ne recréer pas une map (testé et vérifié).
		ground = arcade.Sprite("./map/Tiles/Tiles/ts_grass0/straight/225/0.png", TILE_SCALING)
		ground.center_x = isox
		ground.center_y = isoy
		return ground


	def setEntity(self,pointerToEntity):
		self.isLocked=True
		self.pointerToEntity=pointerToEntity

	@staticmethod  # This decorator means that the method below won't use information from the instance or the class (we don't use "self").
	def cart_to_iso(x, y):
		iso_x = x - y
		iso_y = (x + y) / 2
		return iso_x, iso_y
