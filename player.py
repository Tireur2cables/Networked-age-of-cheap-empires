from CONSTANTS import Resource as Res

class Player:
	def __init__(self,
				IA: bool = True,
				qty_food: int = 200,
				qty_wood: int = 200,
				qty_gold: int = 100,
				qty_stone: int = 200) -> None:
		"""
		Create a player.

		:param bool IA: The player is an IA (True) or a human (False)
		:param int qty[Resource]: The initial qty of the 4 types of Resource
		"""
		self.IA = IA

		# resource (dictionnary initialized with qty[Resource])
		self.resource = {Res.FOOD : qty_food, Res.WOOD : qty_wood, Res.GOLD : qty_gold, Res.STONE : qty_stone}

		# unit
		self.nb_unit = 0
		self.max_unit = 5

	# unit
	def get_nb_unit(self) -> int:
		return self.nb_unit

	def set_nb_unit(self, nb_unit):
		self.nb_unit = nb_unit

	def get_max_unit(self) -> int:
		return self.max_unit

	def set_max_unit(self, nb_max_unit: int):
		self.max_unit = nb_max_unit

	# Resource
	def get_resource(self, resource):
		return self.resource[resource]

	def set_resource(self, resource, total_resource):
		self.resource[resource] = total_resource

	def add_resource(self, resource, qty_resource):
		self.resource[resource] += qty_resource

	def sub_resource(self, resource, qty_resource):
		self.resource[resource] -= qty_resource
