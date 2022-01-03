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
    
	# resource
	#all (par Maxence, le 23/12 à 22h36)
	def add_all(self, qtyRes : int):
		self.resource[Res.FOOD] += qtyRes
		self.resource[Res.WOOD] += qtyRes
		self.resource[Res.GOLD] += qtyRes
		self.resource[Res.STONE] += qtyRes
		
	def reset_all_res(self):
		self.resource[Res.FOOD] += 200
		self.resource[Res.WOOD] += 200
		self.resource[Res.GOLD] += 100
		self.resource[Res.STONE] += 200

	def set_all_res(self, qtyFood, qtyWood, qtyGold, qtyStone):
		self.resource[Res.FOOD] += qtyFood
		self.resource[Res.WOOD] += qtyWood
		self.resource[Res.GOLD] += qtyGold
		self.resource[Res.STONE] += qtyStone
	#food
	def get_food(self) -> int:
		return self.resource[Res.FOOD]

	def set_food(self, totalFood: int):
		self.resource[Res.FOOD] = totalFood

	def add_food(self, qtyFood: int):
		self.resource[Res.FOOD] += qtyFood
	
	def sub_food(self, qtyFood: int):
		self.resource[Res.FOOD] -= qtyFood

	#wood
	def get_wood(self) -> int:
		return self.resource[Res.WOOD]

	def set_wood(self, totalWood: int):
		self.resource[Res.WOOD] = totalWood

	def add_wood(self, qtyWood: int):
		self.resource[Res.WOOD] += qtyWood
	
	def sub_wood(self, qtyWood: int):
		self.resource[Res.WOOD] -= qtyWood
	
	#gold
	def get_gold(self) -> int:
		return self.resource[Res.GOLD]

	def set_gold(self, totalGold: int):
		self.resource[Res.GOLD] = totalGold
    
	# Resource
	def get_resource(self, resource):
		return self.resource[resource]

	def set_resource(self, resource, total_resource):
		self.resource[resource] = total_resource

	def add_resource(self, resource, qty_resource):
		self.resource[resource] += qty_resource

	def sub_resource(self, resource, qty_resource):
		self.resource[resource] -= qty_resource
