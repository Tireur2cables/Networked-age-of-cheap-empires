# --- Imports ---
import arcade
import arcade.gui
from utils.vector import Vector
from utils.isometric import *
from entity.Unit import *
from views.MainView import MainView
from views.CustomButtons import QuitButton
from map.map import Map
from time import sleep

## @tidalwaave : 18/11, 22H30
from entity.Zone import *

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Age Of Cheap Empire"
MUSIC = "./Ressources/music/Marked.mp3"

DEFAULT_MAP_SIZE = 50

#########################################################################
#							MAIN CLASS									#
#########################################################################

class AoCE(arcade.Window):

	def __init__(self):
		""" Initializer """
		# Call the initializer of arcade.Window
		super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=False, fullscreen=False)
		# arcade.set_background_color(arcade.csscolor.WHITE)

		# Show the mouse cursor
		self.set_mouse_visible(True)

		# Lance la musique
		self.my_music = arcade.load_sound(MUSIC, streaming=True)
		self.media_player = self.my_music.play(loop=True)

		self.game_view = GameView()

		# # Variables for communications between model, view and controller.
		# self.toDraw = []

	def on_show(self):
		# Affiche le main menu
		start_view = MainView(self.game_view)
		start_view.setup()
		self.show_view(start_view)

	# Stop all process and exit arcade
	def exit(self):
		self.media_player.delete()
		arcade.exit()

	# Set fulllscreen or defaults : SCREEN_WIDTH x SCREEN_HEIGHT
	def triggerFullscreen(self):
		self.set_fullscreen(not self.fullscreen)

	# Stop or play the music
	def triggerMusic(self):
		if self.media_player.playing:
			self.media_player.pause()
		else:
			self.media_player.play()

	def isPlayingMusic(self):
		return self.media_player.playing


#########################################################################
#							GAME VIEW									#
#########################################################################

class GameView(arcade.View):

	def __init__(self):
		super().__init__()

		# Créer l'architecture MVC
		self.game_model = Model(self)
		self.game_view = View(self)  # Je ne sais pas comment modifier autrement la valeur de "set_mouse_visible"
		self.game_controller = Controller(self)

	def setup(self):
		""" Set up the game and initialize the variables. (Re-called when we want to restart the game without exiting it)."""
		self.game_model.setup()
		self.game_view.setup()
		self.game_controller.setup()

	def on_update(self, *args):  # Redirecting on_update to the Controller
		self.game_controller.on_update(*args)

	def on_key_press(self, *args):
		self.game_view.on_key_press(*args)

	def on_mouse_press(self, *args):  # Redirecting inputs to the View
		self.game_view.on_mouse_press(*args)

	def on_mouse_motion(self, *args):
		self.game_view.on_mouse_motion(*args)

	def on_draw(self):
		self.game_view.on_draw()

	def on_show(self):
		self.game_view.on_show()

	def on_hide_view(self):
		self.manager.disable()

#########################################################################
#							MODEL CLASS									#
#########################################################################

class Model():

	def __init__(self, aoce_game):
		""" Initializer """
		self.game = aoce_game

		self.unit_list = []
		self.tile_list = []
		self.zone_list = []

	def setup(self):

		# Set up the villager and add it to the unit_list.
		self.map = Map(self.tile_list, self.zone_list, DEFAULT_MAP_SIZE)
		unit0 = Villager(Vector(100, 100))
		unit1 = Villager(Vector(50, 50))
		unit2 = Villager(grid_pos_to_iso(Vector(3, 2)) + Vector(0, TILE_HEIGHT_HALF))
		self.unit_list.append(unit0)
		self.unit_list.append(unit1)
		self.unit_list.append(unit2)

		## @tidalwaave : 18/11, 22H30
		# tCent = TownCenter(10, 10)
		# self.zoneLayerList.append(tCent)

#########################################################################
#							VIEW CLASS									#
#########################################################################

# --- Constants ---
CAMERA_MOVE_STEP = 15
CAMERA_MOVE_EDGE = 50

class View():

	def __init__(self, aoce_game):
		""" Initializer """
		self.game = aoce_game

		self.unit_sprite_list = arcade.SpriteList()
		self.tile_sprite_list = arcade.SpriteList()
		self.zone_sprite_list = arcade.SpriteList()

	def setup(self):

		# Variables that will hold sprite lists
		for e in self.game.game_model.unit_list:
			self.unit_sprite_list.append(e.sprite)
		for t in self.game.game_model.tile_list:
			self.tile_sprite_list.append(t.sprite)
		for z in self.game.game_model.zone_list:
			self.zone_sprite_list.append(z.sprite)

	def get_tile_outline(self, map_position):
		left_vertex = tuple(map_position - Vector(TILE_WIDTH//2, 0))
		right_vertex = tuple(map_position + Vector(TILE_WIDTH//2, 0))
		bottom_vertex = tuple(map_position - Vector(0, TILE_HEIGHT//2))
		top_vertex = tuple(map_position + Vector(0, TILE_HEIGHT//2))
		return left_vertex, bottom_vertex, right_vertex, top_vertex

	def draw_grid_position(self, grid_position):
		iso_position = grid_pos_to_iso(grid_position)
		arcade.draw_point(iso_position.x, iso_position.y, (0, 255, 0), 5)

	def draw_iso_position(self, iso_position):
		arcade.draw_point(iso_position.x, iso_position.y, (0, 255, 0), 5)

	def on_draw(self):
		""" Draw everything """
		arcade.start_render()

		# --- Object sprite lists : Tiles, Zones & Entities
		self.tile_sprite_list.draw()

		for i in self.zone_sprite_list:
			i.draw()
			self.draw_iso_position(i.entity.iso_position)

		for i in self.unit_sprite_list:
			if i.selected:
				i.draw_hit_box((255, 0, 0), line_thickness=3)
				map_position = iso_to_grid_pos(i.entity.iso_position)
				# tile_below = self.game.game_model.map.get_tile_at(map_position)
				tile_outline = self.get_tile_outline(grid_pos_to_iso(map_position))
				arcade.draw_polygon_outline(tile_outline, (255, 255, 255))
				# tile_below.sprite.draw_hit_box((255, 0, 0), line_thickness=3)
			i.draw()
			self.draw_iso_position(i.entity.iso_position)

		for x in range(3):
			for y in range(3):
				tile_outline = self.get_tile_outline(grid_pos_to_iso(Vector(x, y)))
				arcade.draw_polygon_outline(tile_outline, (255, 255, 255))
				self.draw_grid_position(Vector(x, y))


		#
		# --- Manager and Camera ---
		#
		self.manager.draw()
		self.camera.use()
		self.camera_move()
		self.camera.move_to([self.camera_x, self.camera_y], 0.5)


	def on_show(self):
		""" This is run once when we switch to this view """

		self.camera = arcade.Camera(self.game.window.width, self.game.window.height)
		initial_x, initial_y = (0, 0)
		self.camera_x = initial_x
		self.camera_y = initial_y

		#coords of the mouse in the middle of the screen by default (and will be update when the mouse will move)
		self.mouse_x = self.game.window.width / 2
		self.mouse_y = self.game.window.height / 2
		#self.set_mouse_visible(False)

		arcade.set_background_color(arcade.csscolor.YELLOW_GREEN)

		# a UIManager to handle the UI.
		self.manager = arcade.gui.UIManager()
		self.manager.enable()

		self.addButton()
		self.addCoordLabel()

	def addButton(self):
		# def button size
		buttonsize = self.game.window.width / 6

		# Create a vertical BoxGroup to align buttons
		self.v_box = arcade.gui.UIBoxLayout()

		# Create the exit button
		quit_button = QuitButton(self.game.window, text="Quit", width=buttonsize)
		self.v_box.add(quit_button)

		# Create a widget to hold the v_box widget, that will center the buttons
		self.manager.add(
			arcade.gui.UIAnchorWidget(
				anchor_x = "left",
				anchor_y = "bottom",
				child = self.v_box
			)
		)

	def addCoordLabel(self):
		coordsize = self.game.window.width / 5

		coordsmouse = f"x = {self.mouse_x}  y = {self.mouse_y}"
		self.coord_label = arcade.gui.UILabel(text = coordsmouse, width= 100, height = 100, anchor_y="bottom")
		coord_label_bg = self.coord_label.with_space_around(5, 5, 5, 5, (20, 20, 20))
		self.max_box = arcade.gui.UIBoxLayout()
		self.max_box.add(self.coord_label)
		self.max_box.add(coord_label_bg)
		self.manager.add(
				arcade.gui.UIAnchorWidget(
				anchor_x = "left",
				anchor_y = "top",
				child = self.max_box
			)
		)
		self.coord_label.fit_content()

	def camera_move(self):
		# Update the camera coords if the mouse is on the edges
		# The movement of the camera is handled in the on_draw() function with move_to()
		if self.mouse_x >= self.game.window.width - CAMERA_MOVE_EDGE:
			self.camera_x += CAMERA_MOVE_STEP
		elif self.mouse_x <= CAMERA_MOVE_EDGE:
			self.camera_x -= CAMERA_MOVE_STEP
		if self.mouse_y <= CAMERA_MOVE_EDGE:
			self.camera_y -= CAMERA_MOVE_STEP
		elif self.mouse_y >= self.game.window.height - CAMERA_MOVE_EDGE:
			self.camera_y += CAMERA_MOVE_STEP

	def on_mouse_press(self, x, y, button, key_modifiers):
		mouse_position_in_game = Vector(x + self.camera.position.x, y + self.camera.position.y)

		if button == arcade.MOUSE_BUTTON_LEFT:
			self.game.game_controller.select(arcade.get_sprites_at_point(tuple(mouse_position_in_game), self.unit_sprite_list))
		elif button == arcade.MOUSE_BUTTON_RIGHT:
			self.game.game_controller.move_selection(mouse_position_in_game)
		elif button == arcade.MOUSE_BUTTON_MIDDLE:
			print(f"position de la souris : {mouse_position_in_game}")
			print(f"position sur la grille : {iso_to_grid_pos(mouse_position_in_game)}")
			pos = mouse_position_in_game
			grid_x = (pos.x / TILE_WIDTH_HALF + pos.y / TILE_HEIGHT_HALF) / 2
			grid_y = (pos.y / TILE_HEIGHT_HALF - (pos.x / TILE_WIDTH_HALF)) / 2
			print(f"position sur la grille sans arrondi : {Vector(grid_x, grid_y)}")

	def on_key_press(self, symbol, modifier):
		if symbol == arcade.key.T:
			mouse_position_in_game = Vector(self.mouse_x + self.camera.position.x, self.mouse_y + self.camera.position.y)
			grid_pos = iso_to_grid_pos(mouse_position_in_game)
			tCent = TownCenter(grid_pos)
			self.game.game_model.zone_list.append(tCent)
			self.zone_sprite_list.append(tCent.sprite)

	def on_mouse_motion(self, x, y, dx, dy):
		"""Called whenever the mouse moves."""
		# Update the coords of the mouse
		self.mouse_x = x
		self.mouse_y = y

		#
		# --- In-game GUI ---
		#
		self.coord_label.text = f"x = {self.mouse_x}  y = {self.mouse_y}"
		self.coord_label.fit_content()


#########################################################################
#							CONTROLLER CLASS							#
#########################################################################

class Controller():
	def __init__(self, aoce_game):
		""" Initializer """
		self.game = aoce_game
		self.pathfinding_matrix = []

		# Selection (will contain elements of type EntitySprite)
		self.selection = set()
		self.moving_sprites = set()

	def setup(self):
		self.pathfinding_matrix = self.game.game_model.map.pathfinding_matrix
		pass

	def is_on_map(self, grid_position):
		return grid_position.x >= 0 and grid_position.x < DEFAULT_MAP_SIZE and grid_position.y >= 0 and grid_position.y < DEFAULT_MAP_SIZE

	def on_update(self, delta_time):

		# @tidalwaave, 19/12, 23h50 : Time to replace the movements methods, fit 'em in tiles
		""" Movement and game logic """

		for sprite in self.moving_sprites:
			# WORKING CODE BELOW
			entity = sprite.entity

			if entity.is_moving:
				# Check if the next position is on the map
				if not self.is_on_map(iso_to_grid_pos(entity.iso_position+entity.change)):
					entity.is_moving = False
				elif entity.iso_position.isalmost(entity.aim, entity.speed):
					if entity.path:
						entity.next_aim()
					else:
						entity.is_moving = False
				else:  # If it is not close to where it aims and not out of bounds, move.
					print(f"change = {entity.change}")
					entity.iso_position += entity.change
					sprite.update()

		if self.moving_sprites:
			self.moving_sprites = {s for s in self.moving_sprites if s.entity.is_moving}


		# END OF WORKING CODE

			# iso_position = iso_to_grid_pos(entity.position)
			# int_position = Vector(int(entity.iso_position.x), int(entity.iso_position.y))
			# int_iso_position = Vector(int(iso_position.x), int(iso_position.y))
			# print(f"{int_position} -> {int_iso_position}")

	def select(self, sprites_at_point):
		print(sprites_at_point)
		sprite = None
		for i in self.selection:
			i.selected = False
		self.selection.clear()
		for i in sprites_at_point:
			if i.entity and isinstance(i.entity, Unit):
				sprite = i
				print(iso_to_grid_pos(i.entity.iso_position))
				break
		if sprite:
			sprite.selected = True
			self.selection.add(sprite)

	def move_selection(self, mouse_position):

		mouse_position_grid = iso_to_grid_pos(mouse_position)

		if self.is_on_map(mouse_position_grid):
			for i in self.selection:
				self.moving_sprites.add(i)
				entity = i.entity

				# Pathfinding algorithm
				grid = Grid(matrix=self.pathfinding_matrix)
				finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
				startvec = iso_to_grid_pos(entity.iso_position)
				endvec = mouse_position_grid
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


# Main function to launch the game
def main():
	""" Main method """
	game = AoCE()
	arcade.run()

if __name__ == "__main__":  # Python syntax that means "if you are launching from this file, run main()", useful if this file is going to be imported.
	main()
