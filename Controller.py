# --- Imports ---
from utils.isometric import *
from entity.Unit import *
from entity.Zone import *
from player import Player

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
		self.player = Player(IA=False)

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

	def move_selection(self, position, need_conversion=True):
		position_grid = position
		if need_conversion:
			position_grid = iso_to_grid_pos(position)
		if self.is_on_map(position_grid):
			for entity in self.selection:
				self.moving_entities.add(entity)

				# Pathfinding algorithm
				pathfinding_matrix = self.game.game_model.map.get_pathfinding_matrix()
				grid = Grid(matrix=pathfinding_matrix)
				finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
				startvec = iso_to_grid_pos(entity.iso_position)
				endvec = position_grid
				start = grid.node(*startvec)
				end = grid.node(*endvec)
				path, runs = finder.find_path(start, end, grid)

				# print(grid.grid_str(path=path, start=start, end=end))
				if path:
					path.pop(0)
					if path:
						entity.set_path(path)
						entity.next_aim()
		else:
			print("out of bound!")

	# Called once when you order an action on a zone
	def action_on_zone(self, mouse_position_in_game):
		for entity in self.selection:
			mouse_grid_pos = iso_to_grid_pos(mouse_position_in_game)
			for z in self.game.game_model.zone_list:
				z_grid_pos = iso_to_grid_pos(z.iso_position)
				if z_grid_pos == mouse_grid_pos:
					print(z)
					entity.aimed_entity = z
					print(z.is_locking)  # This is why villagers can't harvest gold and stone but can harvest trees.
					self.move_selection(z_grid_pos, need_conversion=False)
					break

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
				self.player.add_resource(aimed_entity.get_resource_nbr(), harvested)
				print(self.player.resource)
				entity.aimed_entity = None
				self.dead_entities.add(aimed_entity)
