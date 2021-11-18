from arcade import Sprite


# Wrapper for arcade.Sprite that enables us to access the zone from the sprite.
class ZoneSprite(Sprite):

	def __init__(self, id, zone, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.zone = zone
		zone.sprite = self
		self.id = id
		self.selected = False

