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
	def __init__(self, aoce_game):
		""" Initializer """
		self.game = aoce_game

		# Selection (will contain elements of type Entity)
		self.selection = set()
		self.moving_entities = set()
		self.interacting_entities = set()
		self.dead_entities = set()

	def setup(self):
		pass

	def is_on_map(self, grid_position):
		return grid_position.x >= 0 and grid_position.x < DEFAULT_MAP_SIZE and grid_position.y >= 0 and grid_position.y < DEFAULT_MAP_SIZE

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


		# --- Updating Lists ---
		if self.moving_entities:
			self.moving_entities = {e for e in self.moving_entities if e.is_moving}

		if self.interacting_entities:
			self.interacting_entities = {e for e in self.interacting_entities if e.aimed_entity}


		# --- Deleting dead entities ---
		for dead_entity in self.dead_entities:
			self.discard_entity_from_game(dead_entity)
		self.dead_entities.clear()


	def discard_entity_from_game(self, dead_entity):
		self.selection.discard(dead_entity)
		self.moving_entities.discard(dead_entity)
		self.interacting_entities.discard(dead_entity)
		self.game.game_view.discard_sprite(dead_entity.sprite)
		self.game.game_model.discard_entity(dead_entity)

	def add_entity_to_game(self, new_entity):
		self.game.game_model.add_entity(new_entity)
		self.game.game_view.add_sprite(new_entity.sprite)

	def select(self, sprites_at_point):
		#print(sprites_at_point)
		entity_found = None
		for entity in self.selection:
			entity.selected = False
		self.selection.clear()
		for s in sprites_at_point:
			entity = s.entity
			if entity and isinstance(entity, Unit):
				entity_found = entity
				#print(iso_to_grid_pos(entity.iso_position))
				break
		if entity_found:
			entity_found.selected = True
			self.selection.add(entity_found)
		self.game.game_view.trigger_coin_GUI(self.selection)

	# Called once when you order to move
	def move_selection(self, position, need_conversion=True):
		position_grid = position
		if need_conversion:
			position_grid = iso_to_grid_pos(position)
		if self.is_on_map(position_grid):
			for entity in self.selection:
				self.moving_entities.add(entity)
				path = self.game.game_model.map.get_path(start=iso_to_grid_pos(entity.iso_position), end=position_grid)
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

	# Called once when you order an action on a zone
	def action_on_zone(self, sprites_at_point):
		# Step 1: Search for a zone in the sprites_at_point
		zone_found = None
		for s in sprites_at_point:
			e = s.entity
			if e and isinstance(e, Zone):
				zone_found = e
				break

		if zone_found is not None:
			for entity in self.selection:
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
					self.move_selection(aimed_tile.grid_position, need_conversion=False)

	# Called once
	def build_on_tiles(self, map_position):
		# Step 1: Start moving toward the aimed map_position
		for entity in self.selection:
			entity.action_timer = 0
			can_move = self.move_selection(map_position, need_conversion=False)
			if can_move:
				entity.aimed_entity = House(map_position)


	# Called every frame
	def build_zone(self, entity, delta_time):
		entity.action_timer += delta_time
		if entity.action_timer > entity.aimed_entity.build_time:  # build_time
			entity.action_timer = 0
			self.add_entity_to_game(entity.aimed_entity)
			entity.aimed_entity = None


	# Called every frame when an action is done on a zone (harvesting).
	def harvest_zone(self, entity, delta_time):
		entity.action_timer += delta_time
		if entity.action_timer > 1:
			entity.action_timer = 0
			aimed_entity = entity.aimed_entity
			harvested = aimed_entity.harvest(entity.damage)
			print(f"[harvesting] entity health = {entity.health} - zone health = {aimed_entity.health}")
			if harvested:
				print(f"[harvesting] -> {type(entity).__name__} harvested {harvested} {type(aimed_entity).__name__}!")
				# entity.resource[Resource[type(aimed_entity).__name__.upper()]] = harvested
				# print(entity.resource)
				self.game.player.add_resource(aimed_entity.get_resource_nbr(), harvested)
				self.game.game_view.update_vbox1()
				entity.aimed_entity = None
				self.dead_entities.add(aimed_entity)