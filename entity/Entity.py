from entity.EntitySprite import EntitySprite


#   ______           _     _   _
#  |  ____|         | |   (_) | |
#  | |__     _ __   | |_   _  | |_   _   _
#  |  __|   | '_ \  | __| | | | __| | | | |
#  | |____  | | | | | |_  | | | |_  | |_| |
#  |______| |_| |_|  \__| |_|  \__|  \__, |
#                                     __/ |
#                                    |___/
#

SPRITE_SCALING_COIN = 0.2

class Entity:
	# https://ageofempires.fandom.com/wiki/Units_(Age_of_Empires)
	# https://ageofempires.fandom.com/wiki/Buildings_(Age_of_Empires)
	def __init__(self, position, sprite_image, health=1, damage=0, display=None, rate_fire=1, range=0, melee_armor=0, pierce_armor=0, line_sight=4):

		# Sprite
		self.sprite = EntitySprite(self, filename=sprite_image, scale=SPRITE_SCALING_COIN, center_x=position.x, center_y=position.y, hit_box_algorithm="None")

		# Position
		self.position = position

		#
		## Life
		#
		self.health = health
		self.max_health = health
		self.damage = damage

		#
		## Display
		#
		self.display = display # Nouveau Concept --- Ce concept n'est pas utilisé pour l'instant, peut-être dans le futur cependant

		# Battle
		self.rate_fire = rate_fire
		self.range = range
		self.melee_armor = melee_armor
		self.pierce_armor = pierce_armor
		self.line_sight = line_sight


	# coordonnees
	def get_x(self):
		return self.position.x
	def get_y(self):
		return self.position.y
	def set_xy(self, x, y):
		self.position.x = x
		self.position.y = y

	def get_position(self):
		return self.position
	def set_position(self, position):
		self.position = position

	# health
	def get_health(self):
		return self.health

	def set_health(self, health):
		self.health = health

	def gain_health(self, qty_health):
		self.health += qty_health
		if self.health > self.max_health:# on corrige le nb de pt de vie si celui-ci est superieur au maximum
			self.health = self.max_health

	def lose_health(self, qty_health):
		self.health -= qty_health
		if self.health < 0:# on corrige le nb de pt de vie si celui-ci est negatif
			self.health = 0

	def is_alive(self):
		return self.health > 0

	# max_health
	def get_max_health(self):
		return self.max_health

	def set_max_health(self, max_health):
		self.max_health = max_health

	# damage
	def get_damage(self):
		return self.damage

	def set_damage(self, damage):
		self.damage = damage

	# rate_fire
	def get_rate_fire(self):
		return self.rate_fire

	def set_rate_fire(self, rate_fire):
		self.rate_fire = rate_fire

	# range
	def get_range(self):
		return self.range

	def set_range(self, range):
		self.range = range

	# melee_armor
	def get_melee_armor(self):
		return self.melee_armor

	def set_melee_armor(self, melee_armor):
		self.melee_armor = melee_armor

	# pierce_armor
	def get_pierce_armor(self):
		return self.pierce_armor

	def set_pierce_armor(self, pierce_armor):
		self.pierce_armor = pierce_armor

	# line_sight
	def get_line_sight(self):
		return self.line_sight

	def set_line_sight(self, line_sight):
		self.line_sight = line_sight
