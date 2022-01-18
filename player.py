import random
from CONSTANTS import Resource as Res
from entity.Unit import Unit, Villager
from entity.Zone import BerryBush, Gold, House, Stone, StoragePit, Granary, TownCenter, Wood, WorkSite, Zone
from utils.isometric import iso_to_grid_pos
from utils.vector import Vector

class Player:
	def __init__(self,
				game,
				player_type: str,
				resources: dict) -> None:
		"""
		Create a player.

		:param str player_type: The player can be an human, an IA, ...etc
		:param int qty[Resource]: The initial qty of the 4 types of Resource
		"""
		self.game = game
		self.player_type = player_type

		# resource (dictionnary initialized with qty[Resource]
		# BE CAREFUL: The dictionnary "resources" is the same for all players, this is why we create a new one with this comprehension.
		self.resources = {key: 100000 for key, value in resources.items()}

		# unit
		self.nb_unit = 0
		self.max_unit = 4
		self.town_center = None
		self.my_units = dict()
		self.my_zones = dict()
		self.food_storage = set()
		self.other_storage = set()

	# my_entities
	def add_entity(self, new_entity):
		# Abstract/General class
		if isinstance(new_entity, Unit):
			my_units = self.my_units.get(new_entity.get_name())
			if my_units is None:
				self.my_units[new_entity.get_name()] = set()
			self.my_units[new_entity.get_name()].add(new_entity)

			self.nb_unit += 1

		elif isinstance(new_entity, Zone):
			my_zones = self.my_zones.get(new_entity.get_name())
			if my_zones is None:
				self.my_zones[new_entity.get_name()] = set()
			self.my_zones[new_entity.get_name()].add(new_entity)

			# Concrete class
			if isinstance(new_entity, House):
				self.max_unit += 4
			elif isinstance(new_entity, TownCenter):
				self.town_center = new_entity
				self.food_storage.add(new_entity)
				self.other_storage.add(new_entity)
			elif isinstance(new_entity, Granary):
				self.food_storage.add(new_entity)
			elif isinstance(new_entity, StoragePit):
				self.other_storage.add(new_entity)


	def discard_entity(self, dead_entity):
		if isinstance(dead_entity, Unit):
			self.my_units[dead_entity.get_name()].discard(dead_entity)
			self.nb_unit -= 1
		elif isinstance(dead_entity, Zone):
			self.my_zones[dead_entity.get_name()].discard(dead_entity)
			if isinstance(dead_entity, House):
				self.max_unit -= 4
			elif isinstance(dead_entity, StoragePit):
				self.food_storage.discard(dead_entity)
			elif isinstance(dead_entity, Granary):
				self.other_storage.discard(dead_entity)

	# unit
	def get_nb_unit(self) -> int:
		return self.nb_unit

	def set_nb_unit(self, nb_unit):
		self.nb_unit = nb_unit

	def get_max_unit(self) -> int:
		return self.max_unit

	def set_max_unit(self, nb_max_unit: int):
		self.max_unit = nb_max_unit

	# resource
	#all (par Maxence, le 23/12 à 22h36)
	def add_all(self, qtyRes : int):
		self.resources[Res.FOOD] += qtyRes
		self.resources[Res.WOOD] += qtyRes
		self.resources[Res.GOLD] += qtyRes
		self.resources[Res.STONE] += qtyRes

	def reset_all_res(self):
		self.resources[Res.FOOD] = 200
		self.resources[Res.WOOD] = 200
		self.resources[Res.GOLD] = 100
		self.resources[Res.STONE] = 200

	def set_all_res(self, qtyFood, qtyWood, qtyGold, qtyStone):
		self.resources[Res.FOOD] += qtyFood
		self.resources[Res.WOOD] += qtyWood
		self.resources[Res.GOLD] += qtyGold
		self.resources[Res.STONE] += qtyStone

	# Resource
	def get_resource(self, resource):
		return self.resources[resource]

	def set_resource(self, resource, total_resource):
		self.resources[resource] = total_resource

	def add_resource(self, resource, qty_resource):
		self.resources[resource] += qty_resource

	def sub_resource(self, resource, qty_resource):
		self.resources[resource] -= qty_resource

class AI(Player):
	def __init__(self,
			game,
			player_type: str,
			resources: dict) -> None:
		super().__init__(game, player_type, resources)

	def search_pos_to_build(self, start_position, tile_size):
		area_found = False

		current_iter = 0
		map_position = None
		while not area_found and current_iter < 1000:
			rand_x = random.choice((random.randint(-10, -3), random.randint(3, 10)))
			rand_y = random.choice((random.randint(-10, -3), random.randint(3, 10)))
			map_position = start_position + Vector(rand_x, rand_y)
			area_found = self.game.game_model.map.is_area_empty(map_position, tile_size)
			current_iter += 1
		if current_iter == 1000:
			map_position = None
		print(f"final choice : {map_position}")
		return map_position

	def search_closest_harvest_zone(self, unit, resource):
		class_to_harvest = None
		if resource == "food":
			class_to_harvest = BerryBush
		elif resource == "wood":
			class_to_harvest = Wood
		elif resource == "gold":
			class_to_harvest = Gold
		elif resource == "stone":
			class_to_harvest = Stone

		harvest_zones = {zone for zone in self.game.game_model.zone_list if isinstance(zone, class_to_harvest)}
		aimed_tile, harvest_zone = self.game.game_model.map.get_closest_tile_nearby_collection_fast(iso_to_grid_pos(unit.iso_position), harvest_zones)
		return harvest_zone

	def on_update(self):

		if not self.town_center.is_producing and self.resources[Res.FOOD] > 50:
			self.game.game_controller.order_zone_villagers(self.town_center)

		idle_units = set()
		ongoing_actions = set()
		for unit_list in self.my_units.values():
			for unit in unit_list:
				if not unit.is_moving and not unit.is_interacting:
					idle_units.add(unit)
				else:
					aimed_entity = unit.aimed_entity
					if isinstance(aimed_entity, WorkSite):
						aimed_entity = aimed_entity.zone_to_build
					ongoing_actions.add((unit.goal, aimed_entity.get_name()))

		for unit in idle_units:
			if isinstance(unit, Villager):
				if (action := ("harvest", "berrybush")) not in ongoing_actions and self.resources[Res.FOOD] < 100:
					harvest_zone = self.search_closest_harvest_zone(unit, "food")
					self.game.game_controller.order_harvest(unit, harvest_zone)
					ongoing_actions.add(action)
				elif (action := ("build", "house")) not in ongoing_actions and self.max_unit - self.nb_unit < 2:
					map_position = self.search_pos_to_build(self.town_center.grid_position, House.tile_size)
					self.game.game_controller.order_build(unit, map_position, "House")
					ongoing_actions.add(action)
				elif (action := ("harvest", "wood")) not in ongoing_actions and self.resources[Res.WOOD] < 100:
					harvest_zone = self.search_closest_harvest_zone(unit, "wood")
					self.game.game_controller.order_harvest(unit, harvest_zone)
					ongoing_actions.add(action)
				elif (action := ("harvest", "stone")) not in ongoing_actions and self.resources[Res.STONE] < 100:
					harvest_zone = self.search_closest_harvest_zone(unit, "stone")
					self.game.game_controller.order_harvest(unit, harvest_zone)
					ongoing_actions.add(action)
				elif (action := ("harvest", "gold")) not in ongoing_actions and self.resources[Res.GOLD] < 100:
					harvest_zone = self.search_closest_harvest_zone(unit, "gold")
					self.game.game_controller.order_harvest(unit, harvest_zone)
					ongoing_actions.add(action)
				else:
					pass