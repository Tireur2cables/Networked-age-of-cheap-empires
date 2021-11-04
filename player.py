from CONSTANTS import Resource as Res

class Player:
	def __init__(self,
				IA: bool = True,
				qtyFood: int = 200,
				qtyWood: int = 200,
				qtyGold: int = 100,
				qtyStone: int = 200) -> None:
		"""
		Create a player.

		:param bool IA: The player is an IA (True) or a human (False)
		:param int qty[Resource]: The initial qty of the 4 types of Resource
		"""
		self.IA = IA

		# resource (dictionnary initialized with qty[Resource])
		self.resource = {Res.FOOD : qtyFood, Res.WOOD : qtyWood, Res.GOLD : qtyGold, Res.STONE : qtyStone}
		
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

	def add_gold(self, qtyGold: int):
		self.resource[Res.GOLD] += qtyGold
	
	def sub_gold(self, qtyGold: int):
		self.resource[Res.GOLD] -= qtyGold
	
	#stone
	def get_stone(self) -> int:
		return self.resource[Res.STONE]

	def set_stone(self, totalStone: int):
		self.resource[Res.STONE] = totalStone

	def add_stone(self, qtyStone: int):
		self.resource[Res.STONE] += qtyStone
	
	def sub_stone(self, qtyStone: int):
		self.resource[Res.STONE] -= qtyStone
