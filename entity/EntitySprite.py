from arcade import Sprite


# Wrapper for arcade.Sprite that enables us to access the entity from the sprite.
class EntitySprite(Sprite):

	def __init__(self, id, entity, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.entity = entity
		entity.sprite = self
		self.id = id
		self.selected = False


# class Villager(Unit): # Un Villageois est une Unit particuliere
# 	def __init__(self, position, health=25, damage=3, rate_fire=1.5, range=0, melee_armor=0, pierce_armor=0, line_sight=4, speed=1):
# 		super().__init__(position, health, damage, rate_fire=rate_fire, range=range, melee_armor=melee_armor, pierce_armor=pierce_armor, line_sight=line_sight, speed=speed)
# 		self.resource = {Resource.FOOD : 0, Resource.WOOD : 0, Resource.STONE : 0, Resource.GOLD : 0}#utilisation de l'enumeration Resource
# 		self.max_resource = 10
