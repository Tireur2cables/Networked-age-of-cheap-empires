# --- Imports ---
import arcade
import arcade.gui
from utils.vector import Vector
from entity.Unit import Unit
from entity.EntitySprite import EntitySprite
from views.MainView import MainView
from views.CustomButtons import QuitButton
from map.map import Map

# --- Constants ---
SPRITE_SCALING_COIN = 0.2
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Age Of Cheap Empire"
MUSIC = "./Ressources/music/Marked.mp3"


#########################################################################
#							MAIN CLASS									#
#########################################################################

class AoCE(arcade.Window):

	def __init__(self):
		""" Initializer """
		# Call the initializer of arcade.Window
		super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=False, fullscreen=True)
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

	def on_mouse_press(self, *args):  # Redirecting inputs to the controller
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
		self.entity_list = []

	def setup(self):
		# Set up the villager and add it to the entity_list.
		unit1 = Unit(Vector(50, 50), 10, 10)
		unit2 = Unit(Vector(100, 100), 10, 10)
		self.entity_list.append(unit1)
		self.entity_list.append(unit2)
		pass

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

		# Variables that will hold sprite lists
		self.sprite_list = arcade.SpriteList()
		

	def setup(self):
		for index, item in enumerate(self.game.game_model.entity_list):
			# coin image from kenney.nl
			es = EntitySprite(index, item, "Movements/coin_01.png", SPRITE_SCALING_COIN, center_x=item.position.x, center_y=item.position.y, hit_box_algorithm="None")
			self.sprite_list.append(es)
		# La ligne d'au dessus créer un sprite associé au personnage et le met dans une liste. Le hit_box_algorithm à non c'est pour éviter d'utiliser une hitbox complexe, inutile pour notre projet.
		# "Movements/coin_01.png" may cause an error depending on how the IDE is configurated (what is the root directory). I now how to fix this but haven't implemented it for now.

	def on_draw(self):
		""" Draw everything """
		arcade.start_render()

		self.ground_list.draw()
		self.entity_list.draw()

		for i in self.sprite_list:
			if i.selected:
				i.draw_hit_box((255, 0, 0), line_thickness=3)
			i.draw()
		self.manager.draw()
		self.camera.use()
		self.camera_move()
		self.camera.move_to([self.camera_x, self.camera_y], 0.5)

	def on_show(self):
		""" This is run once when we switch to this view """
		self.ground_list = arcade.SpriteList(use_spatial_hash=True)
		#Should i add an entity list ??? YES !!!!
		self.entity_list = arcade.SpriteList(use_spatial_hash=True)


		self.map = Map(self)
		self.camera = arcade.Camera(self.game.window.width, self.game.window.height)
		initial_x, initial_y = self.map.cart_to_iso(0, 0)
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
		mouse_position = Vector(x + self.camera.position.x, y + self.camera.position.y)

		if button == arcade.MOUSE_BUTTON_LEFT:
			self.game.game_controller.select(arcade.get_sprites_at_point(tuple(mouse_position), self.sprite_list))
		elif button == arcade.MOUSE_BUTTON_RIGHT:
			self.game.game_controller.move_selection(mouse_position)

	def on_mouse_motion(self, x, y, dx, dy):
		"""Called whenever the mouse moves."""
		# Update the coords of the mouse
		self.mouse_x = x
		self.mouse_y = y


#########################################################################
#							CONTROLLER CLASS							#
#########################################################################

class Controller():
	def __init__(self, aoce_game):
		""" Initializer """
		self.game = aoce_game

		# Selection (will be an EntitySprite)
		self.selection = []

	def setup(self):
		pass

	def on_update(self, delta_time):
		""" Movement and game logic """
		for sprite in self.selection:
			entity = sprite.entity
			if not entity.position.isalmost(entity.aim, entity.speed):  # If it is not close to where it aims, move.
				entity.position += entity.change
				sprite.center_x, sprite.center_y = tuple(entity.position)

	def select(self, sprites_at_point):
		for i in self.selection:
			i.selected = False
		self.selection.clear()
		for i in sprites_at_point:
			if i.entity and isinstance(i.entity, Unit):
				sprite = i
				break
		if sprite:
			sprite.selected = True
			self.selection.append(sprite)

	def move_selection(self, mouse_position):
		for i in self.selection:
			entity = i.entity
			# The following calculation is necessary to have uniform speeds :
			entity.aim_towards(mouse_position, entity.speed * ((mouse_position - entity.position).normalized()))
			# We want the same speed no matter what the distance between the villager and where he needs to go is.


# Main function to launche the game
def main():
	""" Main method """
	game = AoCE()
	arcade.run()
