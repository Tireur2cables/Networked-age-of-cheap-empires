# --- Imports ---
import arcade
from arcade.color import BLACK, BROWN_NOSE
import arcade.gui
from utils.vector import Vector
from utils.isometric import *
from entity.Unit import Unit
from entity.EntitySprite import EntitySprite
from views.MainView import MainView
from views.CustomButtons import NextViewButton, ListButton
from map.map import Map
from map.tileSprite import TileSprite
from map.Minimap import Minimap

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
		
	#added by Maxence | 24/12
	def on_key_press(self, key, modifiers):
		if key == arcade.key.F1:
            # User hits f. Flip between full and not full screen.
			self.set_fullscreen(not self.fullscreen)
			width, height = self.get_size()
			self.set_viewport(0, width, 0, height)

	def on_show(self):
		# Affiche le main menu
		start_view = MainView(self.game_view)
		self.game_view.setMenuView(start_view)
		start_view.setup() # useless : mainview.setup is empty
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
		self.menu_view = None
		# Créer l'architecture MVC
		self.game_model = Model(self)
		self.game_view = View(self)  # Je ne sais pas comment modifier autrement la valeur de "set_mouse_visible"
		self.game_controller = Controller(self)

	def setMenuView(self, menu_view) :
		self.menu_view = menu_view

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
		self.game_view.on_hide_view()

#########################################################################
#							MODEL CLASS									#
#########################################################################

class Model():

	def __init__(self, aoce_game):
		""" Initializer """
		self.game = aoce_game

		self.entity_list = []
		self.tile_list = []
		self.zone_list = []

	def setup(self):
		# clear old lists
		self.entity_list.clear()
		self.tile_list.clear()
		self.zone_list.clear()

		# Set up the villager and add it to the entity_list.
		self.map = Map(self.tile_list, DEFAULT_MAP_SIZE)
		unit0 = Unit(Vector(100, 100), 10, 10)
		unit1 = Unit(Vector(50, 50), 10, 10)
		unit2 = Unit(Vector(100, 100), 10, 10)
		self.entity_list.append(unit0)
		self.entity_list.append(unit1)
		self.entity_list.append(unit2)

		## @tidalwaave : 18/11, 22H30
		# tCent = TownCenter(10, 10)
		# self.zoneLayerList.append(tCent)

#########################################################################
#							VIEW CLASS									#
#########################################################################

# --- Constants ---
CAMERA_MOVE_STEP = 15
CAMERA_MOVE_EDGE = 50
COLOR_STATIC_RESSOURCES = (101, 67, 33, 250)
COLOR_STATIC_RESSOURCES_ICONE = arcade.color.DARK_GRAY



# --- Image ressources ---
PIC_CIVIL = "./Ressources/img/Population_500x500.png"
PIC_GOLD = "./Ressources/img/Ressources_Or_500x500.png"
PIC_WOOD = "./Ressources/img/Ressources_Wood_500x500.png"
PIC_STONE = "./Ressources/img/Ressources_Pierre_500x500.png"
PIC_FOOD = "./Ressources/img/Ressources_Viandes_500x500.png"

CAMERA_MOVE_EDGE = 20

class View():

	def __init__(self, aoce_game):
		""" Initializer """
		self.game = aoce_game

		# Variables that will hold sprite lists
		self.entity_sprite_list = arcade.SpriteList()
		self.tile_sprite_list = arcade.SpriteList()
		self.zone_sprite_list = arcade.SpriteList()

	def setup(self) :
		#clear old lists
		self.entity_sprite_list = arcade.SpriteList()
		self.tile_sprite_list = arcade.SpriteList()
		self.zone_sprite_list = arcade.SpriteList()
		# a UIManager to handle the UI.
		self.manager = arcade.gui.UIManager()

		self.init_dynamic_gui()
		self.init_cheats()
		self.sync_entities()
		self.sync_ground()
		self.sync_zones()

	def init_dynamic_gui(self) :
		# Create a box group to align the 'open' button in the center
		self.v_box4 = arcade.gui.UIBoxLayout()
		self.manager.add(
			arcade.gui.UIAnchorWidget(
				anchor_x="right",
				anchor_y="bottom",
				child=self.v_box4
			)
		)
		
		# Create a box for the button in the precedent box, maybe redondant
		self.v_box5 = arcade.gui.UIBoxLayout()
		self.manager.add(
			arcade.gui.UIAnchorWidget(
				anchor_x="right",
				align_x= -100,
				anchor_y="bottom",
				align_y=50,
				child=self.v_box5
			)
		)


	def init_cheats(self) :
		self.display_cheat_input = False

		width = self.game.window.width / 5 # arbitrary
		height = self.game.window.height / 20 # arbitrary
		bg_text = arcade.load_texture("Ressources/img/dark_fond.jpg")
		self.cheat_pane = arcade.gui.UITexturePane(
			arcade.gui.UIInputText(
				x=0,
				y=(self.game.window.height - height) / 2, # middle
				text="enter cheat code here", width=width, height=height,
				text_color=(255, 255, 255, 255)
			),
			tex=bg_text
		)

	def static_menu(self) :
		self.minimap = Minimap(self, DEFAULT_MAP_SIZE, TILE_WIDTH, TILE_HEIGHT,COLOR_STATIC_RESSOURCES)

		# Create a vertical BoxGroup to align buttons
		self.v_box1 = arcade.gui.UIBoxLayout()

		ressources_tab = ["  = 1 ", "  = 5 ", "  = 50 ", "  = 500 ", "  = 5000 "]

		self.HEIGHT_LABEL = self.minimap.size[1] / len(ressources_tab) # in order to have same height as minimap at the end
		self.WIDTH_LABEL = (self.game.window.width / 2) - self.minimap.size[0] - self.HEIGHT_LABEL # moitié - minimap - image

		# Create a text label, contenant le nombre de ressources disponibles pour le joueur
		for val in ressources_tab :
			label = arcade.gui.UITextArea(0, 0, self.WIDTH_LABEL, self.HEIGHT_LABEL, val, text_color=(0, 0, 0, 255), font_name=('Impact',))
			self.v_box1.add(label.with_space_around(0, 0, 0, 0, COLOR_STATIC_RESSOURCES))

		# Create a widget to hold the v_box widget, that will center the buttons
		self.manager.add(
			arcade.gui.UIAnchorWidget(
				anchor_x="left",
				align_x=self.HEIGHT_LABEL + int(self.minimap.size[0]), # just after minimap and icone
				anchor_y="bottom",
				child=self.v_box1
			)
		)

		#Icones des ressources
		self.v_box2 = arcade.gui.UIBoxLayout()

		pics_tab = [PIC_CIVIL, PIC_FOOD, PIC_WOOD, PIC_STONE, PIC_GOLD]
		for val in pics_tab :
			icone = arcade.gui.UITextureButton(x=0, y=0, width=self.HEIGHT_LABEL, height=self.HEIGHT_LABEL, texture=arcade.load_texture(val))
			self.v_box2.add(icone.with_space_around(0, 0, 0, 0, COLOR_STATIC_RESSOURCES_ICONE))

		# Create a widget to hold the v_box widget, that will center the buttons
		self.manager.add(
			arcade.gui.UIAnchorWidget(
				anchor_x="left",
				align_x=int(self.minimap.size[0]), # just after minimap
				anchor_y="bottom",
				child=self.v_box2
			)
		)

	def sync_entities(self):
		# Sync self.game_model.entity_list with sprite_list
		for index, item in enumerate(self.game.game_model.entity_list):
			if item.sprite is None:
				es = EntitySprite(index, item, "Movements/coin_01.png", SPRITE_SCALING_COIN, center_x=item.position.x, center_y=item.position.y, hit_box_algorithm="None")
				self.entity_sprite_list.append(es)
				# La ligne d'au dessus créer un sprite associé au personnage et le met dans une liste. Le hit_box_algorithm à non c'est pour éviter d'utiliser une hitbox complexe, inutile pour notre projet.
				# "Movements/coin_01.png" may cause an error depending on how the IDE is configurated (what is the root directory). I now how to fix this but haven't implemented it for now.

	def sync_ground(self):
		# Sync self.game_model.tile_list with tile_sprite_list
		for index, item in enumerate(self.game.game_model.tile_list):
			if item.sprite is None:
				ts = TileSprite(index, item, TILE_WIDTH, TILE_HEIGHT)
				self.tile_sprite_list.append(ts)

	def sync_zones(self):
		# Sync self.game_model.zone_list with zone_sprite_list
		## @tidalwaave : 18/11, 22H30
		for index, item in enumerate(self.game.game_model.zone_list):
			if item.sprite is None:
				zone_position = map_pos_to_iso(Vector(item.x, item.y), TILE_WIDTH//2, TILE_HEIGHT//2)
				zone = ZoneSprite(index, item, "map/Tower.png", 1, center_x=zone_position.x, center_y=zone_position.y + 253//2 - TILE_HEIGHT, hit_box_algorithm="None", )
				# ATTENTION : la valeur numérique 253 est une valeur issue du sprite
				self.zone_sprite_list.append(zone)

	def on_draw(self):
		""" Draw everything """
		arcade.start_render()

		#
		# --- Object sprite lists : Tiles, Zones & Entities
		#
		self.tile_sprite_list.draw()

		self.zone_sprite_list.draw()

		for i in self.entity_sprite_list:
			if i.selected:
				i.draw_hit_box((255, 0, 0), line_thickness=3)
				map_position = iso_to_map_pos(i.entity.position, TILE_WIDTH//2, TILE_HEIGHT//2)
				tile_below = self.game.game_model.map.get_tile_at(map_position.int())
				tile_below.sprite.draw_hit_box((255, 0, 0), line_thickness=3)
			i.draw()

		# Update the minimap
		self.minimap.draw()

		#
		# --- In-game GUI ---
		#
		self.coord_label.text = f"x = {self.mouse_x}  y = {self.mouse_y}"
		self.coord_label.fit_content()

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

		self.manager.enable()

		self.static_menu()
		self.addButton()
		self.addCoordLabel()

	def addButton(self):
		# def button size
		buttonsize = self.game.window.width / 6 # arbitrary

		# Create a vertical BoxGroup to align buttons
		self.v_box3 = arcade.gui.UIBoxLayout()

		# Create the exit button
		retour_button = NextViewButton(self.game.window, self.game.menu_view, text="Menu", width=buttonsize)
		# Create the save button
		save_button = NextViewButton(self.game.window, self.game.menu_view, text="Sauvegarder", width=buttonsize)

		# Create the option button
		option_button = ListButton(self.v_box3, [save_button, retour_button], text="Option", width=buttonsize)
		self.v_box3.add(option_button)

		# Create a widget to hold the v_box widget, that will center the buttons
		self.manager.add(
			arcade.gui.UIAnchorWidget(
				anchor_x = "right",
				anchor_y = "top",
				child = self.v_box3
			)
		)

	def addCoordLabel(self): # just for debug (should disappear for the final render)
		coordsize = self.game.window.width / 5 # arbitrary?

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

	def camera_move(self) :
		# Update the camera coords if the mouse is on the edges
		# The movement of the camera is handled in the on_draw() function with move_to()
		if self.mouse_x >= self.game.window.width - CAMERA_MOVE_EDGE :
			self.camera_x += CAMERA_MOVE_STEP
		elif self.mouse_x <= CAMERA_MOVE_EDGE :
			self.camera_x -= CAMERA_MOVE_STEP
		if self.mouse_y <= CAMERA_MOVE_EDGE :
			self.camera_y -= CAMERA_MOVE_STEP
		elif self.mouse_y >= self.game.window.height - CAMERA_MOVE_EDGE :
			self.camera_y += CAMERA_MOVE_STEP

	def on_mouse_press(self, x, y, button, key_modifiers) :
		mouse_position = Vector(x + self.camera.position.x, y + self.camera.position.y)
		if self.minimap.is_on_minimap_sprite(x, y) :
			self.camera_x = (x * DEFAULT_MAP_SIZE * TILE_WIDTH / self.minimap.size[0]) - ((DEFAULT_MAP_SIZE * TILE_WIDTH) / 2) - self.camera.viewport_width / 2
			self.camera_y = (y * DEFAULT_MAP_SIZE * TILE_HEIGHT / self.minimap.size[1]) - self.camera.viewport_height / 2
			self.camera.move_to([self.camera_x, self.camera_y], 1)
		elif button == arcade.MOUSE_BUTTON_LEFT :
			self.game.game_controller.select(arcade.get_sprites_at_point(tuple(mouse_position), self.entity_sprite_list))
		elif button == arcade.MOUSE_BUTTON_RIGHT:
			self.game.game_controller.move_selection(mouse_position)

	def on_key_press(self, symbol, modifier):
		if symbol == arcade.key.T:
			mouse_position_on_map = Vector(self.mouse_x, self.mouse_y) + Vector(self.camera.position.x, self.camera.position.y)
			pos = iso_to_map_pos(mouse_position_on_map, TILE_WIDTH//2, TILE_HEIGHT//2).int()
			tCent = TownCenter(pos.x, pos.y)
			print(pos)
			self.game.game_model.zone_list.append(tCent)
			self.sync_zones()
		elif symbol == arcade.key.F10 :
			self.triggerCheatInput()

	def on_mouse_motion(self, x, y, dx, dy):
		"""Called whenever the mouse moves."""
		# Update the coords of the mouse
		self.mouse_x = x
		self.mouse_y = y

	def triggerCheatInput(self) :
		if self.display_cheat_input :
			self.manager.remove(self.cheat_pane)
		else :
			self.manager.add(self.cheat_pane)
		self.display_cheat_input = not self.display_cheat_input

	#En construction, marche paaaaaaaaas des masses
	def trigger_coin_GUI(self, selected_list) :
		self.v_box4.clear()
		self.v_box5.clear()



		if selected_list :
			width = self.game.window.width / 2 # other half of the screen
			height = self.minimap.size[1] # same as minimap
			coin_box = arcade.gui.UITextArea(text="Coin I Chiwa", width=width, height=height)
			self.v_box4.add(coin_box.with_space_around(0, 0, 0, 0, arcade.color.BRONZE))

			# Button for coin, you wan click on it but unfortunately, it will unselect the coin which result in the disapearance of the button
			coin_button = arcade.gui.UIFlatButton(text = "Machala")
			self.v_box5.add(coin_button.with_space_around(0,0,0,0,arcade.color.ANTIQUE_BRONZE))

	def on_hide_view(self) :
		self.manager.disable()

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
			if i.entity and isinstance(i.entity, Unit) :
				sprite = i
				break
		if sprite:
			sprite.selected = True
			self.selection.append(sprite)

		self.game.game_view.trigger_coin_GUI(self.selection)


	def move_selection(self, mouse_position):
		for i in self.selection:
			entity = i.entity
			# The following calculation is necessary to have uniform speeds :
			entity.aim_towards(mouse_position, entity.speed * ((mouse_position - entity.position).normalized()))
			# We want the same speed no matter what the distance between the villager and where he needs to go is.


# Main function to launch the game
def main():
	""" Main method """
	game = AoCE()
	arcade.run()
