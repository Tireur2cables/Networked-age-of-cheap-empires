class Zone:
	def __init__(self, x, y):#constructeur : initialise les attributs
		self.x = x
		self.y = y
		self.sprite = None

# Getting and setting coordinates from the building
	def set_x(self, x):
		self.x = x

	def get_x(self):
		return self.x

	def set_y(self, y):
		self.y = y

	def get_y(self):
		return self.y
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
		super().__init__(x, y, health)

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


