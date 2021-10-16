from utils.vector import Vector

class Entity:
	# https://ageofempires.fandom.com/wiki/Units_(Age_of_Empires)
	# https://ageofempires.fandom.com/wiki/Buildings_(Age_of_Empires)
	def __init__(self, position, health, damage, display=None, rate_fire=1, range=0, melee_armor=0, pierce_armor=0, line_sight=4):
		# Position
		self.position = position

		# Life
		self.health = health
		self.max_health = health
		self.damage = damage

		# Display
		self.display = display # Nouveau Concept --- Ce concept n'est pas utilisé pour l'instant, peut-être dans le futur cependant

		# Battle
		self.rate_fire = rate_fire
		self.range = range
		self.melee_armor = melee_armor
		self.pierce_armor = pierce_armor
		self.line_sight = line_sight

		# Movement
		self.aim = Vector(0, 0)  # coordinate aimed by the user when he clicked
		self.change = Vector(0, 0)  # The change of coordinate calculated from the speed. This may be moved in the Controller in the future.
		self.speed = 5  # Speed of the villager (should probably be a constant)


	# coordonnees
	def get_x(self):
		return self.position.x
	def get_y(self):
		return self.position.y
	def get_position(self):
		return self.position

	def set_position(self, x, y):
		self.position.x = x
		self.position.y = y

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

	# Function for movement, may change in the future when pathfinding will be needed.
	def aim_towards(self, aim):
		self.aim = aim
		# The following calculation is necessary to have uniform speeds :
		self.change = self.speed * ((self.aim - self.position).normalized())
		# We want the same speed no matter what the distance between the villager and where he needs to go is.
