# Imports
import arcade
import arcade.gui
from views.CustomButtons import QuitButton, NextViewButton, CheckboxButton
import random

#############################################################
#						Main View							#
#############################################################

# Constants
BACKGROUND = "./Ressources/img/background.png"

# View d'accueil : première à etre affichée à l'écran
class MainView(arcade.View) :

	def on_show(self):
		""" This is run once when we switch to this view """

		# ajoute l'image de background
		self.texture = arcade.load_texture(BACKGROUND)

		# add an UIManager to handle the UI.
		self.manager = arcade.gui.UIManager()
		self.manager.enable()

		self.setupButtons()

	def setupButtons(self):
		# def button size
		buttonsize = self.window.width / 6

		# Create a vertical BoxGroup to align buttons
		self.v_box = arcade.gui.UIBoxLayout()

		# Create the buttons
		start_button = NextViewButton(self.window, FakeGameView(), text="Start Game", width=buttonsize)
		self.v_box.add(start_button.with_space_around(bottom=20))

		map_button = NextViewButton(self.window, GameView(), text="Show Map", width=buttonsize)
		self.v_box.add(map_button.with_space_around(bottom=20))

		settings_button = NextViewButton(self.window, SettingsView(), text="Settings", width=buttonsize)
		self.v_box.add(settings_button.with_space_around(bottom=20))

		quit_button = QuitButton(self.window, text="Quit", width=buttonsize)
		self.v_box.add(quit_button)

		# Create a widget to hold the v_box widget, that will center the buttons
		self.manager.add(
			arcade.gui.UIAnchorWidget(
				anchor_x = "left",
				align_x = buttonsize,
				anchor_y = "center_y",
				child = self.v_box
			)
		)

	def on_draw(self):
		""" Draw this view """

		arcade.start_render()
		self.texture.draw_sized(self.window.width / 2, self.window.height / 2, self.window.width, self.window.height)
		self.manager.draw()

	def on_hide_view(self) :
		self.manager.disable()

#############################################################
#						Settings View						#
#############################################################

# Constants
SETTINGS_BACKGROUND = "./Ressources/img/LastImageSettings.jpg"

# View des paramètres accessible via ecran d'accueil
class SettingsView(arcade.View) :
	""" Settings view """

	def on_show(self):
		""" This is run once when we switch to this view """

		# ajoute l'image de background
		self.texture = arcade.load_texture(SETTINGS_BACKGROUND)

		# a UIManager to handle the UI.
		self.manager = arcade.gui.UIManager()
		self.manager.enable()

		self.setupButtons()

	def setupButtons(self) :
		# def sizes
		buttonsize = self.window.width / 6
		checkboxsize = buttonsize / 2

		# Create a vertical BoxGroup to align buttons
		self.v_box = arcade.gui.UIBoxLayout()

		# Create checkboxes
		music_button = CheckboxButton(self.window, text="Musique", size=checkboxsize, ticked=self.window.isPlayingMusic(), music=True)
		self.v_box.add(music_button.with_space_around(bottom=20))

		fullscreen_button = CheckboxButton(self.window, text="Plein écran", size=checkboxsize, ticked=self.window.fullscreen, fullscreen=True)
		self.v_box.add(fullscreen_button.with_space_around(bottom=20))

		# Create the return menu
		retour_button = NextViewButton(self.window, MainView(), text="Retour", width=buttonsize)
		self.v_box.add(retour_button.with_space_around(bottom=20))

		# Create a widget to hold the v_box widget, that will center the buttons
		self.manager.add(
			arcade.gui.UIAnchorWidget(
				anchor_x = "center_x",
				anchor_y = "center_y",
				child = self.v_box
			)
		)

	def on_draw(self):
		""" Draw this view """
		arcade.start_render()

		self.texture.draw_sized(self.window.width / 2, self.window.height / 2, self.window.width, self.window.height)
		arcade.draw_text("Settings Screen", self.window.width / 2, self.window.height * 5 / 6, arcade.color.WARM_BLACK, font_size=50, anchor_x="center")

		self.manager.draw()


	def on_hide_view(self) :
		self.manager.disable()

#########################################################################
#							GAME VIEW									#
#########################################################################

# --- Constants ---
CHARACTER_SCALING = 1
TILE_SCALING = 1
TILE_SIZE = 64

CAMERA_MOVE_STEP = 15
CAMERA_MOVE_EDGE = 50

class GameView(arcade.View) :

	def __init__(self) :
		super().__init__()

		# Créer l'architecture MVC
		self.game_model = Model(self)
		self.game_view = View(self)  # Je ne sais pas comment modifier autrement la valeur de "set_mouse_visible"
		self.game_controller = Controller(self)
		self.setup()

	def setup(self) :
		""" Set up the game and initialize the variables. (Re-called when we want to restart the game without exiting it)."""
		self.game_model.setup()
		self.game_view.setup()
		self.game_controller.setup()

	def on_update(self, *args):  # Redirecting on_update to the Controller
		self.game_controller.on_update(*args)

	def on_mouse_press(self, *args):  # Redirecting inputs to the controller
		self.game_controller.on_mouse_press(*args)

	def on_mouse_motion(self, *args):
		self.game_view.on_mouse_motion(*args)

	def on_draw(self):
		self.game_view.on_draw()

	def on_show(self):
		self.game_view.on_show()

	def on_hide_view(self) :
		self.manager.disable()

#########################################################################
#							MODEL CLASS									#
#########################################################################

class Model() :

	def __init__(self, aoce_game) :
		""" Initializer """
		self.game = aoce_game
		# self.entity_list = []

	def setup(self) :
		# Set up the villager and add it to the entity_list.
		# unit1 = Unit(Vector(50, 50), 10, 10)
		# unit2 = Unit(Vector(100, 100), 10, 10)
		# self.entity_list.append(unit1)
		# self.entity_list.append(unit2)
		pass

#########################################################################
#							VIEW CLASS									#
#########################################################################

class View() :

	def __init__(self, aoce_game) :
		""" Initializer """
		self.game = aoce_game

		# Variables that will hold sprite lists
		# self.sprite_list = arcade.SpriteList()

	def setup(self) :
		# for index, item in enumerate(self.game.game_model.entity_list):
		# 	# coin image from kenney.nl
		# 	self.sprite_list.append(EntitySprite(index, item, "Movements/coin_01.png", SPRITE_SCALING_COIN, center_x=item.position.x, center_y=item.position.y, hit_box_algorithm="None"))
		# La ligne d'au dessus créer un sprite associé au personnage et le met dans une liste. Le hit_box_algorithm à non c'est pour éviter d'utiliser une hitbox complexe, inutile pour notre projet.
		# "Movements/coin_01.png" may cause an error depending on how the IDE is configurated (what is the root directory). I now how to fix this but haven't implemented it for now.
		pass

	def on_draw(self):
		""" Draw everything """
		"""Render the screen."""
		arcade.start_render()
		self.ground_list.draw()
		self.manager.draw()
		self.camera.use()
		self.camera_move()
		self.camera.move_to([self.camera_x, self.camera_y], 0.5)
		# self.sprite_list.draw()

	def on_show(self) :
		""" This is run once when we switch to this view """

		self.camera = arcade.Camera(self.game.window.width, self.game.window.height)
		initial_x, initial_y = self.cart_to_iso(0, 0)
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

		self.generateMap()

		self.addButton()

	def generateMap(self) :
		# def offset
		#offset = 4 * self.window.width // 3

		self.ground_list = arcade.SpriteList(use_spatial_hash=True)

		for x in range(0, self.game.window.width, 40) :
			for y in range(0, self.game.window.width, 40) :
				isox, isoy = self.cart_to_iso(x, y)
				ground = arcade.Sprite("./map/Tiles/Tiles/ts_grass0/straight/225/0.png", TILE_SCALING)
				ground.center_x = isox
				ground.center_y = isoy
				self.ground_list.append(ground)

	def addButton(self) :
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

	# Convert cartesian coordinates to isometric
	def cart_to_iso(self, x, y) :
		iso_x = x - y
		iso_y = (x + y)/2
		return iso_x, iso_y

	def camera_move(self):
		#update the camera coords if the mouse is on the edges
		#the moving of the camera is in the on_draw() function with move_to()
		if self.mouse_x >= self.game.window.width - CAMERA_MOVE_EDGE:
			self.camera_x += CAMERA_MOVE_STEP
		elif self.mouse_x <= CAMERA_MOVE_EDGE:
			self.camera_x -= CAMERA_MOVE_STEP
		if self.mouse_y <= CAMERA_MOVE_EDGE:
			self.camera_y -= CAMERA_MOVE_STEP
		elif self.mouse_y >= self.game.window.height - CAMERA_MOVE_EDGE:
			self.camera_y += CAMERA_MOVE_STEP

	def on_mouse_motion(self, x, y, dx, dy) :
		"""Called whenever the mouse moves."""
		#update the coords of the mouse
		self.mouse_x = x
		self.mouse_y = y

	# def get_sprite_list(self):
	# 	return self.sprite_list

#########################################################################
#							CONTROLLER CLASS							#
#########################################################################

class Controller() :
	def __init__(self, aoce_game) :
		""" Initializer """
		self.game = aoce_game

		# # Selection (will be an EntitySprite)
		# self.selection = []

	def setup(self) :
		pass

	def on_update(self, delta_time) :
	# 	""" Movement and game logic """
	# 	for sprite in self.selection:
	# 		entity = sprite.entity
	# 		if not entity.position.isalmost(entity.aim, entity.speed):  # If it is not close to where it aims, move.
	# 			entity.position += entity.change
	# 			sprite.center_x, sprite.center_y = tuple(entity.position)
		pass

	def on_mouse_press(self, x, y, button, key_modifiers):
	# 	mouse_position = Vector(x, y)
	#
	# 	if button == arcade.MOUSE_BUTTON_RIGHT:
	# 		for i in self.selection:
	# 			i.entity.aim_towards(mouse_position)
	# 			print(mouse_position)
	#
	# 	elif button == arcade.MOUSE_BUTTON_LEFT:
	# 		self.selection.clear()
	# 		villagers = arcade.get_sprites_at_point(tuple(mouse_position), self.game.game_view.get_sprite_list())
	# 		if villagers:
	# 			self.selection.append(villagers[0])  # ou -1, jsp encore si c'est celui qui est tout derrière ou celui qui est tout devant là.
		pass

#############################################################
#					Fake Game								#
#############################################################

# --- Constants ---
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_COIN = .25
COIN_COUNT = 50
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Age Of Cheap Empire"

class FakeGameView(arcade.View):
	""" Our custom Window Class"""

	def __init__(self):
		""" Initializer """
		# Call the parent class initializer
		super().__init__()

		# Variables that will hold sprite lists
		self.player_list = None
		self.coin_list = None

		# Set up the player info
		self.player_sprite = None
		self.score = 0

	def on_show(self):
		""" Set up the game and initialize the variables. """
		arcade.set_background_color(arcade.color.AMAZON)

		# Don't show the mouse cursor
		self.window.set_mouse_visible(False)

		# Sprite lists
		self.player_list = arcade.SpriteList()
		self.coin_list = arcade.SpriteList()

		# Score
		self.score = 0

		# Set up the player
		# Character image from kenney.nl
		self.player_sprite = arcade.Sprite(":resources:images/animated_characters/female_person/femalePerson_idle.png", SPRITE_SCALING_PLAYER)
		self.player_sprite.center_x = 50
		self.player_sprite.center_y = 50
		self.player_list.append(self.player_sprite)

		# Create the coins
		for i in range(COIN_COUNT):

			# Create the coin instance
			# Coin image from kenney.nl
			coin = arcade.Sprite(":resources:images/items/coinGold.png", SPRITE_SCALING_COIN)

			# Position the coin
			coin.center_x = random.randrange(SCREEN_WIDTH)
			coin.center_y = random.randrange(SCREEN_HEIGHT)

			# Add the coin to the lists
			self.coin_list.append(coin)

	def on_draw(self):
		""" Draw everything """
		arcade.start_render()
		self.coin_list.draw()
		self.player_list.draw()

		# Put the text on the screen.
		output = f"Score: {self.score}"
		arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

	def on_mouse_motion(self, x, y, dx, dy):
		""" Handle Mouse Motion """

		# Move the center of the player sprite to match the mouse x, y
		self.player_sprite.center_x = x
		self.player_sprite.center_y = y

	def on_update(self, delta_time):
		""" Movement and game logic """

		# Call update on all sprites (The sprites don't do much in this
		# example though.)
		self.coin_list.update()

		# Generate a list of all sprites that collided with the player.
		coins_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)

		# Loop through each colliding sprite, remove it, and add to the score.
		for coin in coins_hit_list:
			coin.remove_from_sprite_lists()
			self.score += 1
