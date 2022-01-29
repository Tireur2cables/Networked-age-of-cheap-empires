# --- Imports ---
from utils.isometric import *
from entity.Unit import *
from entity.Zone import *

# --- Constants ---
from CONSTANTS import DEFAULT_MAP_SIZE, Resource

#########################################################################
#							CONTROLLER CLASS							#
#########################################################################

class Controller():

# --- Setup ---

	def __init__(self, aoce_game):
		""" Initializer """
		self.game = aoce_game

		# Selection (will contain elements of type Entity)
		self.selection = dict()  # self.section ---> convert to a dict, the key is "player" or "ai_1" or "ai_2" or ...
		self.dead_entities = set()

	def setup(self, players):
		for p in players:
			self.selection[p] = set()



# --- Utility methods ---
	@staticmethod
	def filter_type(type):
		return lambda entity: isinstance(entity, type)
	@staticmethod
	def filter_faction(faction):
		return lambda entity: entity.faction == faction
	@staticmethod
	def filter_both(type, faction):
		return lambda entity: isinstance(entity, type) and entity.faction == faction

	@staticmethod
	def find_entity_in_sprites(sprites_collection, filter):
		for s in sprites_collection:
			entity = s.entity
			if entity and filter(entity):
				return entity
		return None
	@staticmethod
	def find_entity(entity_collection, filter):
		for e in entity_collection:
			if e and filter(e):
				return e
		return None



# --- Adding/Discarding entities ---

	def add_entity_to_game(self, new_entity):
		player = self.game.players.get(new_entity.faction)
		if player is not None:
			player.add_entity(new_entity)
		self.game.game_model.add_entity(new_entity)
		self.game.game_view.add_sprite(new_entity.sprite)
		self.game.game_view.update_resources_gui()

	def discard_entity_from_game(self, dead_entity):
		if (selection_set := self.selection.get(dead_entity.faction)):
			selection_set.discard(dead_entity)
		self.game.game_view.update_resources_gui()

		player = self.game.players.get(dead_entity.faction)
		if player is not None:
			player.discard_entity(dead_entity)
		self.game.game_view.discard_sprite(dead_entity.sprite)
		self.game.game_model.discard_entity(dead_entity)



# --- Selection (Called once) ---

	def select(self, faction, sprites_at_point):
		self.clear_faction_selection(faction)
		unit_found = self.find_entity_in_sprites(sprites_at_point, self.filter_type(Unit))
		if unit_found :
			unit_found.selected = True
			self.selection[faction].add(unit_found)

	def select_zone(self, faction, sprites_at_point):
		self.clear_faction_selection(faction)
		zone_found = self.find_entity_in_sprites(sprites_at_point, self.filter_type(Zone))
		if zone_found:
			zone_found.selected = True
			self.selection[faction].add(zone_found)

	def clear_faction_selection(self, faction):
		for entity in self.selection[faction]:
			entity.selected = False
		self.selection[faction].clear()

	def unit_in_selection(self, faction):
		for entity in self.selection[faction]:
			if isinstance(entity, Unit):
				return True
		return False

	def zone_in_selection(self, faction):
		for entity in self.selection[faction]:
			if isinstance(entity, Zone):
				return True
		return False



# --- Human Orders (Called once) ----

	def human_order_towards_sprites(self, action, faction, sprites_at_point):
		for entity in self.selection[faction]:
			if isinstance(entity, Villager):
				if action == "harvest":
					zone_found = self.find_entity_in_sprites(sprites_at_point, self.filter_type(Resources))
					if zone_found:
						self.order_harvest(entity, zone_found)
				elif action == "stock":
					zone_found = self.find_entity_in_sprites(sprites_at_point, self.filter_type((TownCenter, StoragePit, Granary)))
					if zone_found:
						self.order_stock_resources(entity, zone_found)

	def human_order_towards_position(self, action, faction, iso_position, *args):
		grid_position = iso_to_grid_pos(iso_position)
		for entity in self.selection[faction]:
			if isinstance(entity, Unit) and entity.faction == faction :
				if action == "move":
					entity.set_goal("move")
					if self.is_on_map(grid_position):
						for entity in self.selection[faction]:
							self.move_entity(entity, grid_position)
					else:
						print("out of bound!")
						return
				elif action == "build":
					self.order_build(entity, grid_position, *args)

	def human_order_with_zone(self, action, faction):
		if action == "populate":
			for entity in self.selection[faction]:
				if entity.faction == faction and isinstance(entity, TownCenter):
					self.order_zone_villagers(entity)



# --- Orders (Called once) ----
	def move_entity(self, entity, grid_position):
		path, path_len = self.game.game_model.map.get_path(start=iso_to_grid_pos(entity.iso_position), end=grid_position)
		if path_len > 0:
			entity.set_move_action()
			entity.set_path(path)
			entity.next_aim()
		else:
			return

	# Called once when you order an action on a zone
	def order_harvest(self, entity, zone_to_harvest):
		entity_grid_pos = iso_to_grid_pos(entity.iso_position)

		# Step 1: Search the closest tile near the zone_found to harvest it.
		aimed_tile = self.game.game_model.map.get_closest_tile_nearby(entity_grid_pos, iso_to_grid_pos(zone_to_harvest.iso_position))

		# Step 2: Start moving toward the aimed entity
		if aimed_tile is not None:
			entity.set_goal("harvest")
			entity.set_aimed_entity(zone_to_harvest)
			if aimed_tile.grid_position == entity_grid_pos: # Dans ce cas c'est que nous sommes déjà arrivé
				entity.is_interacting = True
			else:
				self.move_entity(entity, aimed_tile.grid_position)

	def order_search_stock_resources(self, entity, resource_nbr):
		entity_grid_pos = iso_to_grid_pos(entity.iso_position)
		if resource_nbr == Res.FOOD:
			stock_zones = self.game.players[entity.faction].food_storage
		else:
			stock_zones = self.game.players[entity.faction].other_storage

		aimed_tile, stock_zone = self.game.game_model.map.get_closest_tile_nearby_collection(entity_grid_pos, stock_zones)
		print(aimed_tile, stock_zone)
		# Step 2: Start moving toward the aimed entity
		if aimed_tile is not None:
			entity.set_aimed_entity(stock_zone)
			if aimed_tile.grid_position == entity_grid_pos:
				entity.set_aimed_entity(stock_zone)
			else:
				self.move_entity(entity, aimed_tile.grid_position)


	def order_stock_resources(self, entity, stock_zone):
		entity_grid_pos = iso_to_grid_pos(entity.iso_position)

		# Step 1: Search the closest tile near the zone_found to harvest it.
		aimed_tile = self.game.game_model.map.get_closest_tile_nearby(entity_grid_pos, stock_zone.grid_position)

		# Step 2: Start moving toward the aimed entity
		if aimed_tile is not None:
			entity.set_aimed_entity(stock_zone)
			if aimed_tile.grid_position == entity_grid_pos:
				entity.set_aimed_entity(stock_zone)
			else:
				self.move_entity(entity, aimed_tile.grid_position)

	# Called once
	def order_build(self, entity, map_position, building_name):
		# Step 1: Create a worksite with the building_name
		worksite = WorkSite(map_position, entity.faction, building_name)
		if self.game.players[entity.faction].get_resource(worksite.zone_to_build.cost[0]) >= worksite.zone_to_build.cost[1]:
			# Step 2: Search for an entity that can build: a Villager.
			if isinstance(entity, Villager):
				# Step 3: Start searching if it is possible to move toward the aimed map_position
				for i in range(worksite.zone_to_build.tile_size[0]):
					for j in range(worksite.zone_to_build.tile_size[1]):
						tile = self.game.game_model.map.get_tile_at(map_position + Vector(i, j))
						if tile.pointer_to_entity is not None or tile.is_free == 0:
							return
				# Step 4: if possible (no return), move one tile below the first tile of the building.
				entity.set_goal("build")
				entity.set_aimed_entity(worksite)
				aim = map_position - Vector(1,1)

				if iso_to_grid_pos(entity.iso_position) == aim:
					entity.is_interacting = True
				else:
					self.move_entity(entity, map_position - Vector(1, 1))
			else:
				print("Not a Villager!")
		else:
			print("not enough resources to build!")

	def order_zone_villagers(self, tc):
		current_player = self.game.players[tc.faction]
		if not tc.is_producing and current_player.get_resource(tc.villager_cost[0]) >= tc.villager_cost[1] and current_player.nb_unit < current_player.max_unit:
			tc.is_producing = True
			current_player.sub_resource(tc.villager_cost[0], tc.villager_cost[1])
			if tc.faction == "player" : # Shouldn't be used with AI
				self.game.game_view.update_resources_gui()



# --- On_update (Called every frame) ---

	def on_update(self, delta_time):
		""" Movement and game logic """

		# --- Updating Sets ---
		moving_entities = set()
		interacting_entities = set()
		for e in self.game.game_model.unit_list:
			if e.is_moving:
				moving_entities.add(e)
			if e.is_interacting:
				interacting_entities.add(e)

		producing_entities = set()
		for e in self.game.game_model.zone_list:
			if isinstance(e, TownCenter) and e.is_producing:
				producing_entities.add(e)

		# --- Action - Moving entities ---
		for entity in moving_entities:
			# Check if the next position is on the map
			if not self.is_on_map(iso_to_grid_pos(entity.iso_position+entity.change)):
				entity.is_moving = False
				print("OUT OF BOUND !!!")
			elif entity.iso_position.isalmost(entity.aim, entity.speed):
				if entity.path:
					entity.next_aim()
				else: # ça veut dire qu'il est arrivé
					entity.is_moving = False
					if entity.goal in ("harvest", "stock", "build"):
						entity.is_interacting = True

			else:  # If it is not close to where it aims and not out of bounds, move.
				entity.iso_position += entity.change
				entity.sprite.update()

		# --- Action - Interacting entities ---
		for entity in interacting_entities:
			if isinstance(entity.aimed_entity, Resources):
				self.harvest_zone(entity, delta_time)
			elif isinstance(entity.aimed_entity, WorkSite):
				self.build_zone(entity, delta_time)
			elif isinstance(entity.aimed_entity, (TownCenter, StoragePit, Granary)):
				self.stock_resources(entity, entity.aimed_entity.get_name())

		for entity in producing_entities:
			if isinstance(entity, TownCenter):
				self.produce_villagers(entity, delta_time)

		# --- Deleting dead entities ---
		for dead_entity in self.dead_entities:
			self.discard_entity_from_game(dead_entity)
		self.dead_entities.clear()

	def is_on_map(self, grid_position):
		return grid_position.x >= 0 and grid_position.x < DEFAULT_MAP_SIZE and grid_position.y >= 0 and grid_position.y < DEFAULT_MAP_SIZE



# --- Updating interaction (Called every frame) ---

	# Called every frame
	def build_zone(self, entity, delta_time):
		entity.action_timer += delta_time
		if entity.action_timer > entity.aimed_entity.zone_to_build.build_time:  # build_time
			entity.action_timer = 0

			current_player = self.game.players[entity.faction]
			cost = entity.aimed_entity.zone_to_build.cost
			current_player.sub_resource(*cost)
			if entity.faction == "player" :
				self.game.game_view.update_resources_gui()

			self.add_entity_to_game(entity.aimed_entity.create_zone())

			entity.end_goal()

	# Called every frame when an action is done on a zone (harvesting).
	# Récupère les resources présentes à chaque seconde, jusqu'à ce que ce soit full. Dans ce cas, il doit retourner au Town Center
	def harvest_zone(self, entity, delta_time):
		entity.action_timer += delta_time
		if entity.action_timer > 1:
			entity.action_timer = 0
			aimed_entity = entity.aimed_entity
			print(f"[harvesting] zone health = {aimed_entity.health} - zone amount = {aimed_entity.amount}")
			if not entity.is_full():
				harvested = aimed_entity.harvest(entity.damage)
				if harvested > 0:
					entity.resource[aimed_entity.get_resource_nbr()] += harvested
					print(f"[harvesting] -> {type(entity).__name__} harvested {harvested} {type(aimed_entity).__name__}!")
					print(f"[harvesting] -> {type(entity).__name__} has {entity.resource} - max_resources : {entity.max_resource}")
					if entity.faction == "player" :
						self.game.game_view.update_villager_resources_gui()
				elif harvested == -1: # The zone is totaly harvested.
					entity.end_goal()
					self.dead_entities.add(aimed_entity)
			else: # the entity is full and needs to go back to the town center.
				entity.set_goal("stock")
				self.order_search_stock_resources(entity, aimed_entity.get_resource_nbr())

	# Stock les resources qui ont été récolté définitivement et s'arrête
	def stock_resources(self, entity, storage_type):
		items_to_store = ()
		if storage_type == "towncenter":
			items_to_store = (Res.FOOD, Res.GOLD, Res.STONE, Res.WOOD)
		elif storage_type == "granary":
			items_to_store = (Res.FOOD,)
		elif storage_type == "storage_pit":
			items_to_store = (Res.GOLD, Res.STONE, Res.WOOD)

		for resource in items_to_store:
			self.game.players[entity.faction].add_resource(resource, entity.resource[resource])
			self.game.game_view.update_resources_gui()
			entity.resource[resource] = 0
		can_harvest = entity.go_back_to_harvest()
		if can_harvest:
			self.order_harvest(entity, entity.previous_aimed_entity)



	# produit un villageois et s'arrête
	def produce_villagers(self, tc, delta_time):
		tc.action_timer += delta_time
		if tc.action_timer > tc.villager_cooldown:
			tc.action_timer = 0
			tc.is_producing = False
			grid_position = iso_to_grid_pos(tc.iso_position) - Vector(1, 1)
			self.add_entity_to_game(Villager(grid_pos_to_iso(grid_position), tc.faction))
