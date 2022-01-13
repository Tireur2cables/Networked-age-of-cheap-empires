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
		unit_found = self.find_entity_in_sprites(sprites_at_point, self.filter_both(Unit, faction))
		self.clear_faction_selection(faction)
		if unit_found is not None:
			unit_found.selected = True
			self.selection[faction].add(unit_found)
			self.game.game_view.trigger_coin_GUI(self.selection)

	def select_zone(self, faction, sprites_at_point):
		self.clear_faction_selection(faction)
		zone_found = self.find_entity_in_sprites(sprites_at_point, self.filter_faction(faction))
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



# --- Order (Called once) ----

	def order_towards_sprites(self, action, faction, sprites_at_point):
		for entity in self.selection[faction]:
			if isinstance(entity, Villager):
				if action == "harvest":
					zone_found = self.find_entity_in_sprites(sprites_at_point, self.filter_type(Resources))
					if zone_found:
						self.order_harvest(entity, zone_found)
				elif action == "stock":
					zone_found = self.find_entity_in_sprites(sprites_at_point, self.filter_type(TownCenter))
					if zone_found:
						self.order_stock_resources(entity, zone_found)

	def order_towards_position(self, action, faction, iso_position, *args):
		grid_position = iso_to_grid_pos(iso_position)
		for entity in self.selection[faction]:
			if isinstance(entity, Unit):
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
		# Step 1: Search for a zone in the sprites_at_point


		# Step 2: Search the closest tile near the zone_found to harvest it.
		entity_grid_pos = iso_to_grid_pos(entity.iso_position)
		aimed_tile = self.game.game_model.map.get_closest_tile_nearby(entity_grid_pos, iso_to_grid_pos(zone_to_harvest.iso_position))

		# Step 3: Start moving toward the aimed entity
		if aimed_tile is not None:
			entity.set_goal("harvest")
			entity.set_aimed_entity(zone_to_harvest)
			if aimed_tile.grid_position == entity_grid_pos: # Dans ce cas c'est que nous sommes déjà arrivé
				entity.is_interacting = True
			else:
				self.move_entity(entity, aimed_tile.grid_position)

	def order_stock_resources(self, entity, stock_zone):
		# Step 2: Search the closest tile near the zone_found to harvest it.
		entity_grid_pos = iso_to_grid_pos(entity.iso_position)

		aimed_tile = self.game.game_model.map.get_closest_tile_nearby(entity_grid_pos, iso_to_grid_pos(stock_zone.iso_position))

		# Step 3: Start moving toward the aimed entity
		if aimed_tile is not None:
			entity.set_aimed_entity(stock_zone)
			if aimed_tile.grid_position == entity_grid_pos:
				entity.set_aimed_entity(stock_zone)
			else:
				self.move_entity(entity, aimed_tile.grid_position)

	# Called once
	def order_build(self, entity, map_position, building_name):
		# Step 1: Find which building building_name is
		worksite = WorkSite(map_position, entity.faction, building_name)
		if self.game.players[entity.faction].get_resource(worksite.zone_to_build.cost[0]) > worksite.zone_to_build.cost[1]:
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

	def order_zone_villagers(self, faction):
		for entity in self.selection[faction]:
			if isinstance(entity, TownCenter):
				tc = entity
				current_player = self.game.players[faction]
				if not tc.is_producing and current_player.get_resource(tc.villager_cost[0]) > tc.villager_cost[1] and current_player.nb_unit < current_player.max_unit:
					tc.is_producing = True
					current_player.sub_resource(tc.villager_cost[0], tc.villager_cost[1])  # TODO CONVERT FOR AI
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
			elif isinstance(entity.aimed_entity, TownCenter):
				self.stock_resources(entity)

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
			if current_player.get_resource(cost[0]) > cost[1]:
				current_player.sub_resource(*cost)
				self.game.game_view.update_resources_gui()
				self.add_entity_to_game(entity.aimed_entity.create_zone())
			else:
				print("not enough resources to build!")

			entity.end_goal()

	# Called every frame when an action is done on a zone (harvesting).
	# Récupère les resources présentes à chaque seconde, jusqu'à ce que ce soit full. Dans ce cas, il doit retourner
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
					self.game.game_view.update_resources_gui()
				elif harvested == -1: # The zone is totaly harvested.
					entity.end_goal()
					self.dead_entities.add(aimed_entity)
			else: # the entity is full and needs to go back to the town center.
				entity.set_goal("stock")
				stock_zone = next(iter(self.game.players[entity.faction].my_entities["towncenter"]))
				self.order_stock_resources(entity, stock_zone)

	# Stock les resources qui ont été récolté définitivement et s'arrête
	def stock_resources(self, entity):
		for resource, resource_val in entity.resource.items():
			self.game.players[entity.faction].add_resource(resource, resource_val)
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
