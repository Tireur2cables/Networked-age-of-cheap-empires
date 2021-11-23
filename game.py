# --- Imports ---
import arcade
import arcade.gui
from utils.vector import Vector
from utils.isometric import *
from entity.Unit import Unit
from entity.EntitySprite import EntitySprite
from views.MainView import MainView
from views.CustomButtons import QuitButton
from map.map import Map
from map.tileSprite import TileSprite

## @tidalwaave : 18/11, 22H30
from entity.Zone import *
from entity.ZoneSprite import ZoneSprite

# --- Constants ---
SPRITE_SCALING_COIN = 0.2
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Age Of Cheap Empire"
MUSIC = "./Ressources/music/Marked.mp3"

DEFAULT_MAP_SIZE = 50

TILE_WIDTH = 64
TILE_HEIGHT = TILE_WIDTH // 2


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
		self.ground_list = []
		## @tidalwaave : 18/11, 22H30
		self.zoneLayerList = []

	def setup(self):

		# Set up the villager and add it to the entity_list.
		self.map = Map(self, DEFAULT_MAP_SIZE)
		unit0 = Unit(Vector(100, 100), 10, 10)
		unit1 = Unit(Vector(50, 50), 10, 10)
		unit2 = Unit(Vector(100, 100), 10, 10)
		self.entity_list.append(unit0)
		self.entity_list.append(unit1)
		self.entity_list.append(unit2)


		## @tidalwaave : 18/11, 22H30
		# tCent = TownCenter(10, 10)
		# self.zoneLayerList.append(tCent)



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
		self.tile_sprite_list = arcade.SpriteList()

		## @tidalwaave : 18/11, 22H30
		self.zoneLayerSpriteList = arcade.SpriteList()

	def setup(self):
		self.sync_entities()
		self.sync_ground()
		self.sync_zones()


	def sync_entities(self):
		for index, item in enumerate(self.game.game_model.entity_list): # Sync self.game_model.entity_list with sprite_list
			if item.sprite is None:
				es = EntitySprite(index, item, "Movements/coin_01.png", SPRITE_SCALING_COIN, center_x=item.position.x, center_y=item.position.y, hit_box_algorithm="None")
				self.sprite_list.append(es)
				# La ligne d'au dessus créer un sprite associé au personnage et le met dans une liste. Le hit_box_algorithm à non c'est pour éviter d'utiliser une hitbox complexe, inutile pour notre projet.
				# "Movements/coin_01.png" may cause an error depending on how the IDE is configurated (what is the root directory). I now how to fix this but haven't implemented it for now.

	def sync_ground(self): # Sync self.game_model.ground_list with tile_sprite_list
		for index, item in enumerate(self.game.game_model.ground_list):
			if item.sprite is None:
				ts = TileSprite(index, item, TILE_WIDTH, TILE_HEIGHT)
				self.tile_sprite_list.append(ts)

	def sync_zones(self): # Sync self.game_model.zoneLayerList with zoneLayerSpriteList
		## @tidalwaave : 18/11, 22H30
		for index, item in enumerate(self.game.game_model.zoneLayerList):
			if item.sprite is None:
				zone_position = map_pos_to_iso(Vector(item.x, item.y), TILE_WIDTH//2, TILE_HEIGHT//2)
				zone = ZoneSprite(index, item, "map/Tower.png", 1, center_x=zone_position.x, center_y=zone_position.y + 253//2 - TILE_HEIGHT, hit_box_algorithm="None", )
				self.zoneLayerSpriteList.append(zone)

	def on_draw(self):
		""" Draw everything """
		arcade.start_render()

		self.tile_sprite_list.draw()


		## @tidalwaave : 18/11, 22H30
		self.zoneLayerSpriteList.draw()

		for i in self.sprite_list:
			if i.selected:
				i.draw_hit_box((255, 0, 0), line_thickness=3)
				map_position = iso_to_map_pos(i.entity.position, TILE_WIDTH//2, TILE_HEIGHT//2)
				tile_below = self.game.game_model.map.get_tile_at(map_position.int())
				tile_below.sprite.draw_hit_box((255, 0, 0), line_thickness=3)
			i.draw()
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

	def on_key_press(self, symbol, modifier):
		if symbol == arcade.key.T:
			mouse_position_on_map = Vector(self.mouse_x, self.mouse_y) + Vector(self.camera.position.x, self.camera.position.y)
			pos = iso_to_map_pos(mouse_position_on_map, TILE_WIDTH//2, TILE_HEIGHT//2).int()
			tCent = TownCenter(pos.x, pos.y)
			print(pos)
			self.game.game_model.zoneLayerList.append(tCent)
			self.sync_zones()

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
			next_map_position = iso_to_map_pos(entity.position+entity.change, TILE_WIDTH//2, TILE_HEIGHT//2).int()
			next_is_on_map = next_map_position.x >= 0 and next_map_position.x < DEFAULT_MAP_SIZE and next_map_position.y >= 0 and next_map_position.y < DEFAULT_MAP_SIZE
			if (not entity.position.isalmost(entity.aim, entity.speed)) and next_is_on_map:  # If it is not close to where it aims, move.
				entity.position += entity.change
				sprite.center_x, sprite.center_y = tuple(entity.position)

			# iso_position = iso_to_map_pos(entity.position, TILE_WIDTH//2, TILE_HEIGHT//2)
			# int_position = Vector(int(entity.position.x), int(entity.position.y))
			# int_iso_position = Vector(int(iso_position.x), int(iso_position.y))
			# print(f"{int_position} -> {int_iso_position}")

	def select(self, sprites_at_point):
		sprite = None
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
