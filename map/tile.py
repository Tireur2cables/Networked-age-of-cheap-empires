
import arcade
from map.arcadeDisplay import cartToIso

# --- Constants ---
CHARACTER_SCALING = 1
TILE_SCALING = 1
TILE_SIZE = 64
TILE_DIST = TILE_SIZE // 2


class Tile():
	def __init__(self, blockID, isLocked, tileCoord, pointerToEntity):
		self.blockID = blockID
		self.isLocked = isLocked
		self.tileCoord = tileCoord
		self.pointerToEntity = pointerToEntity
		self.tileSprite=None
		

	def generateSprite(self, blockID):
		self.tileSprite = arcade.Sprite("./map/Tiles/Tiles/ts_grass0/straight/225/0.png", TILE_SCALING)
		self.tileSprite.center_x=40*self.tileCoord.x
		self.tileSprite.center_y=40*self.tileCoord.y
		isox, isoy = cartToIso(x,y)  # Cette ligne ne recréer pas une map (testé et vérifié).

	@staticmethod  # This decorator means that the method below won't use information from the instance or the class (we don't use "self").
	def cart_to_iso(x, y):
		iso_x = x - y
		iso_y = (x + y) / 2
		return iso_x, iso_y
