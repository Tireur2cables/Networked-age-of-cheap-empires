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
		self.moving_entities = set()
		self.interacting_entities = set()
		self.producing_entities = set()
		self.dead_entities = set()

	def setup(self, players):
		for p in players:
			self.selection[p] = set()



# --- Adding/Discarding entities ---

	def add_entity_to_game(self, new_entity):
		self.game.game_model.add_entity(new_entity)
		self.game.game_view.add_sprite(new_entity.sprite)

	def discard_entity_from_game(self, dead_entity):
		if (selection_set := self.selection.get(dead_entity.faction)):
			selection_set.discard(dead_entity)
		self.moving_entities.discard(dead_entity)
		self.interacting_entities.discard(dead_entity)
		self.producing_entities.discard(dead_entity)
		self.game.game_view.discard_sprite(dead_entity.sprite)
		self.game.game_model.discard_entity(dead_entity)



# --- Selection (Called once) ---

	def select(self, faction, sprites_at_point):
		self.clear_faction_selection(faction)
		#print(sprites_at_point)
		unit_found = None
		for s in sprites_at_point:
			entity = s.entity
			if entity and isinstance(entity, Unit) and entity.faction == faction:
				unit_found = entity
				#print(iso_to_grid_pos(entity.iso_position))
				break
		if unit_found:
			unit_found.selected = True
			self.selection[faction].add(unit_found)
		self.game.game_view.trigger_coin_GUI(self.selection)

	def select_zone(self, faction, sprites_at_point):
		self.clear_faction_selection(faction)
		zone_found = None
		for s in sprites_at_point:
			zone = s.entity
			if zone.faction == faction:
				zone_found = zone
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

	# Called once when you setup the movement of the selection
	def move_selection(self, faction, grid_position):
		if self.is_on_map(grid_position):
			for entity in self.selection[faction]:
				self.moving_entities.add(entity)
				path = self.game.game_model.map.get_path(start=iso_to_grid_pos(entity.iso_position), end=grid_position)
				# print(grid.grid_str(path=path, start=start, end=end))
				if path:
					path.pop(0)
					if path:
						entity.set_path(path)
						entity.next_aim()
						return True
					else:
						return False
				else:
					return False
		else:
			print("out of bound!")
			return False

	# Called once when you order to move
	def order_move(self, faction, iso_position):
		grid_position = iso_to_grid_pos(iso_position)
		found_entity = False
		for entity in self.selection[faction]:
			if isinstance(entity, Unit):
				entity.aimed_entity = None
				found_entity = True
				break
		if found_entity:
			self.move_selection(faction, grid_position)

	# Called once when you order an action on a zone
	def order_harvest(self, faction, sprites_at_point):
		# Step 1: Search for a zone in the sprites_at_point
		zone_found = None
		for s in sprites_at_point:
			e = s.entity
			if e and isinstance(e, Zone):
				zone_found = e
				break

		if zone_found is not None:
			for entity in self.selection[faction]:
				if isinstance(entity, Villager):
					# Step 2: Search the closest tile near the zone_found to harvest it.
					z_grid_pos = iso_to_grid_pos(zone_found.iso_position)

					aimed_tile = None
					min_path_len = DEFAULT_MAP_SIZE**2  # Value that shouldn't be reached when searching a path through the map.
					entity_grid_position = iso_to_grid_pos(entity.iso_position)
					for tile in self.game.game_model.map.get_tiles_nearby(z_grid_pos):
						path = self.game.game_model.map.get_path(entity_grid_position, tile.grid_position)
						if path:
							path.pop()
							if path:
								path_len = len(path)
								if min_path_len > path_len:
									aimed_tile = tile
									min_path_len = path_len
							else:
								self.interacting_entities.add(entity)
								entity.aimed_entity = zone_found
								aimed_tile = None
								break

					# Step 3: Start moving toward the aimed entity
					if aimed_tile is not None:
						entity.action_timer = 0
						entity.aimed_entity = zone_found
						self.move_selection(faction, aimed_tile.grid_position)
				else:
					print("Not a villager!")

	# Called once
	def order_build(self, faction, map_position, building_name):
		# Step 1: Find which building building_name is
		building = None
		if building_name == "House":
			building = House(map_position, faction)
		elif building_name == "StoragePit":
			building = StoragePit(map_position, faction)
		elif building_name == "Granary":
			building = Granary(map_position, faction)
		elif building_name == "Barracks":
			building = Barracks(map_position, faction)
		elif building_name == "Dock":
			building = Dock(map_position, faction)

		assert isinstance(building, Buildable)

		if self.game.player.get_resource(building.cost[0]) > building.cost[1]:  # TODO CONVERT FOR AI

			# Step 2: Search for an entity that can build: a Villager.
			for entity in self.selection[faction]:
				if isinstance(entity, Villager):
					entity.action_timer = 0
					entity.aimed_entity = building
					# Step 3: Start searching if it is possible to move toward the aimed map_position
					for i in range(entity.aimed_entity.tile_size[0]):
						for j in range(entity.aimed_entity.tile_size[1]):
							tile = self.game.game_model.map.get_tile_at(map_position + Vector(i, j))
							if tile.pointer_to_entity is not None or tile.is_free == 0:
								entity.aimed_entity = None
								return
					# Step 4: if possible (no return), move one tile below the first tile of the building.
					self.move_selection(faction, map_position - Vector(1, 1))
				else:
					print("Not a Villager!")
		else:
			print("not enough resources to build!")

	def order_zone_villagers(self, faction):
		for entity in self.selection[faction]:
			if isinstance(entity, TownCenter):
				tc = entity
				if not tc.is_producing and self.game.player.get_resource(tc.villager_cost[0]) > tc.villager_cost[1]:
					tc.is_producing = True
					self.game.player.sub_resource(tc.villager_cost[0], tc.villager_cost[1])  # TODO CONVERT FOR AI
					self.game.game_view.update_resources_gui()
					self.producing_entities.add(tc)



# --- On_update (Called every frame) ---

	def on_update(self, delta_time):
		""" Movement and game logic """

		# --- Action - Moving entities ---
		for entity in self.moving_entities:
			if entity.is_moving:
				# Check if the next position is on the map
				if not self.is_on_map(iso_to_grid_pos(entity.iso_position+entity.change)):
					entity.is_moving = False
				elif entity.iso_position.isalmost(entity.aim, entity.speed):
					if entity.path:
						entity.next_aim()
					else:
						entity.is_moving = False
						if entity.aimed_entity:
							self.interacting_entities.add(entity)

				else:  # If it is not close to where it aims and not out of bounds, move.
					entity.iso_position += entity.change
					entity.sprite.update()

		# --- Action - Interacting entities ---
		for entity in self.interacting_entities:
			if isinstance(entity.aimed_entity, Resources):
				self.harvest_zone(entity, delta_time)
			elif isinstance(entity.aimed_entity, Buildable):
				self.build_zone(entity, delta_time)

		for entity in self.producing_entities:
			if isinstance(entity, TownCenter):
				self.produce_villagers(entity, delta_time)

		# --- Updating Lists ---
		if self.moving_entities:
			self.moving_entities = {e for e in self.moving_entities if e.is_moving}

		if self.interacting_entities:
			self.interacting_entities = {e for e in self.interacting_entities if e.aimed_entity}

		if self.producing_entities:
			self.producing_entities = {e for e in self.producing_entities if e.is_producing}


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
		if entity.action_timer > entity.aimed_entity.build_time:  # build_time
			if self.game.player.get_resource(entity.aimed_entity.cost[0]) > entity.aimed_entity.cost[1]:  # TODO CONVERT FOR AI
				self.game.player.sub_resource(*entity.aimed_entity.cost)  # TODO CONVERT FOR AI
				self.game.game_view.update_resources_gui()
				self.add_entity_to_game(entity.aimed_entity)
			else:
				print("not enough resources to build!")
			entity.action_timer = 0
			entity.aimed_entity = None

	# Called every frame when an action is done on a zone (harvesting).
	def harvest_zone(self, entity, delta_time):
		entity.action_timer += delta_time
		if entity.action_timer > 1:
			entity.action_timer = 0
			aimed_entity = entity.aimed_entity
			print(f"[harvesting] zone health = {aimed_entity.health} - zone amount = {aimed_entity.amount}")
			harvested = aimed_entity.harvest(entity.damage)
			if harvested > 0:
				print(f"[harvesting] -> {type(entity).__name__} harvested {harvested} {type(aimed_entity).__name__}!")
				# entity.resource[Resource[type(aimed_entity).__name__.upper()]] = harvested
				# print(entity.resource)
				self.game.player.add_resource(aimed_entity.get_resource_nbr(), harvested)  # TODO CONVERT FOR AI
				self.game.game_view.update_resources_gui()
			elif harvested == -1:
				entity.aimed_entity = None
				self.dead_entities.add(aimed_entity)

	def produce_villagers(self, tc, delta_time):
		tc.action_timer += delta_time
		if tc.action_timer > tc.villager_cooldown:
			tc.action_timer = 0
			tc.is_producing = False
			grid_position = iso_to_grid_pos(tc.iso_position) - Vector(1, 1)
			self.add_entity_to_game(Villager(grid_pos_to_iso(grid_position), tc.faction))
