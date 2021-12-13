from entity.Entity import Entity
from entity.ZoneSprite import ZoneSprite
TILE_WIDTH = 64
TILE_HEIGHT = TILE_WIDTH // 2

class Zone(Entity):
	def __init__(self, x, y, tileSize):#constructeur : initialise les attributs
		self.tileSize=tileSize
		self.sprite = ZoneSprite(self, "map/Tower.png", 1, center_x=x, center_y=y + 253//2 - TILE_HEIGHT, hit_box_algorithm="None")


# Zone : Base brick of something that is present on the map, and not IN the map
#        Has a position, appears and disappears from the map
#
#
# Subclasses of Zone :
# Buildable : Civil, Military, Economic (no subclass & no need to differenciate)
# Resources (Natural !) : Mines, trees,
# Between both : buildable resources (champs)

# Tasklist :
# Town Center
# Buisson cueillette





#FILE NAMING CONVENTION : Zone_Buildable_TownCenter.py IN SUBFOLDERS ????


#   ____        _ _     _       _     _
#  |  _ \      (_) |   | |     | |   | |
#  | |_) |_   _ _| | __| | __ _| |__ | | ___
#  |  _ <| | | | | |/ _` |/ _` | '_ \| |/ _ \
#  | |_) | |_| | | | (_| | (_| | |_) | |  __/
#  |____/ \__,_|_|_|\__,_|\__,_|_.__/|_|\___|
class Buildable(Zone):
	def __init__(self, x, y, health):
		super().__init__(x, y) # Calls parent class constructor
		self.health = health
		self.maxhealth = health


	def set_health(self, health):
		self.health = health
	def get_health(self):
		return self.health

	def set_maxhealth(self):
		return self.maxhealth
	def get_maxhealth(self):
		return self.maxhealth

# intégrer préconditions de construction de bat dans bat qui permet de construire bat
# avancées tech : fonction boucle faisant appel aux fonctions des objets respectifs pour modif leur propriétés

#
##
### Town Center
##
#
class TownCenter(Buildable):
	#WhoAmI : Cost : 200Wood 60sec build time
	#Size: 3x3
	#LineOfSight : 7
	def __init__(self, x, y, health = 600):
		super().__init__(x, y, health, tileSize=(3,3))
		self.set_line_sight(7)

	def get_health(self):
		return self.health

class Barracks(Buildable):
		#WhoAmI : Cost : 125Wood and 30sec buildtime; Train & Upgrade infantry (Clubman)
	def __init__(self, x, y, health = 350):
		super().__init__(x, y, health)

	def get_health(self):
		return self.health

class StoragePit(Buildable):
		#WhoAmI : Cost : 120 Wood, 30sec Build time; Use : Drop off wood, stone,gold (& food from hunt & fishing ONLY)
		#Size : 3x3
		#LineOfSight:4
	def __init__(self, x, y, health = 350):
		super().__init__(x, y, health)

	def get_health(self):
		return self.health

class Granary(Buildable):
		#WhoAmI : Cost : 120 Wood, 30 sec build time; Use : Drop off Food from Gatherers, Foragers & Farmers (subclass Villager)
	def __init__(self, x, y, health = 350):
		super().__init__(x, y, health)

	def get_health(self):
		return self.health

class Dock(Buildable):
		#WhoAmI : Cost : 100 Wood; Use : Train & upgrade ships
	def __init__(self, x, y, health = 600):
		super().__init__(x, y, health)

	def get_health(self):
		return self.health

class House(Buildable):
		#WhoAmI : Cost : 30 Wood; Use : +4 population per house
	def __init__(self, x, y, health = 75):
		super().__init__(x, y, health)

	def get_health(self):
		return self.health



#  ______
#  | ___ \
#  | |_/ /  ___  ___   ___   _   _  _ __   ___   ___  ___
#  |    /  / _ \/ __| / _ \ | | | || '__| / __| / _ \/ __|
#  | |\ \ |  __/\__ \| (_) || |_| || |   | (__ |  __/\__ \
#  \_| \_| \___||___/ \___/  \__,_||_|    \___| \___||___/
#
#
class Resources(Zone):
	def __init__(self, x, y, health, amount):
		super().__init__(x, y) # Calls parent class constructor
		self.health = health
		self.maxhealth = health
		self.amount = amount


	def set_health(self, health):
		self.health = health
	def get_health(self):
		return self.health

	def set_maxhealth(self):
		return self.maxhealth
	def get_maxhealth(self):
		return self.maxhealth

	def set_amount(self, amount):
		self.amount = amount
	def get_amount(self):
		return self.amount

class Wood(Resources):
	def __init__(self, x, y):
		super().__init__(x,y,25,75)
