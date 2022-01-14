from CONSTANTS import Resource as Res
from entity.Unit import Unit
from entity.Zone import House, StoragePit, Granary, TownCenter

class Player:
	def __init__(self,
				game,
				player_type: str,
				qty_food: int = 200,
				qty_wood: int = 200,
				qty_gold: int = 100,
				qty_stone: int = 200) -> None:
		"""
		Create a player.

		:param str player_type: The player can be an human, an IA, ...etc
		:param int qty[Resource]: The initial qty of the 4 types of Resource
		"""
		self.game = game
		self.player_type = player_type

		# resource (dictionnary initialized with qty[Resource])
		self.resource = {Res.FOOD : qty_food, Res.WOOD : qty_wood, Res.GOLD : qty_gold, Res.STONE : qty_stone}

		# unit
		self.nb_unit = 0
		self.max_unit = 4
		self.my_entities = dict()
		self.food_storage = set()
		self.other_storage = set()


	def setup(self, resources):
		self.resource = resources

	# my_entities
	def add_entity(self, new_entity):
		my_entities = self.my_entities.get(new_entity.get_name())
		if my_entities is None:
			self.my_entities[new_entity.get_name()] = set()
		self.my_entities[new_entity.get_name()].add(new_entity)

		if isinstance(new_entity, Unit):
			self.nb_unit += 1
		elif isinstance(new_entity, House):
			self.max_unit += 4
		elif isinstance(new_entity, TownCenter):
			self.food_storage.add(new_entity)
			self.other_storage.add(new_entity)
		elif isinstance(new_entity, Granary):
			self.food_storage.add(new_entity)
		elif isinstance(new_entity, StoragePit):
			self.other_storage.add(new_entity)

	def discard_entity(self, dead_entity):
		self.my_entities[dead_entity.get_name()].discard(dead_entity)

		if isinstance(dead_entity, Unit):
			self.nb_unit -= 1
		elif isinstance(dead_entity, House):
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
		self.resource[Res.FOOD] += qtyRes
		self.resource[Res.WOOD] += qtyRes
		self.resource[Res.GOLD] += qtyRes
		self.resource[Res.STONE] += qtyRes

	def reset_all_res(self):
		self.resource[Res.FOOD] = 200
		self.resource[Res.WOOD] = 200
		self.resource[Res.GOLD] = 100
		self.resource[Res.STONE] = 200

	def set_all_res(self, qtyFood, qtyWood, qtyGold, qtyStone):
		self.resource[Res.FOOD] += qtyFood
		self.resource[Res.WOOD] += qtyWood
		self.resource[Res.GOLD] += qtyGold
		self.resource[Res.STONE] += qtyStone

	# Resource
	def get_resource(self, resource):
		return self.resource[resource]

	def set_resource(self, resource, total_resource):
		self.resource[resource] = total_resource

	def add_resource(self, resource, qty_resource):
		self.resource[resource] += qty_resource

	def sub_resource(self, resource, qty_resource):
		self.resource[resource] -= qty_resource
