# --- Imports ---
import arcade
from arcade.color import BLACK, BROWN_NOSE
import arcade.gui
from utils.vector import Vector
from utils.isometric import *
from entity.Unit import *
from views.MainView import MainView
from views.CustomButtons import ConstructButton, NextViewButton, ListButton, QuitButton, SaveButton
from map.map import Map
from map.tileSprite import TileSprite
from map.Minimap import Minimap
from cheats.fonctions import CheatsInput
from map.MapCreationindependantprojet.abstract_perlin_matrix import perlin_array,process_array
from save.serializationTest import *
from entity.Zone import *

# --- Constants ---
from CONSTANTS import Resource as Res
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

	def on_mouse_press(self, *args):  # Redirecting inputs to the View
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

		self.unit_list = []
		self.tile_list = []
		self.zone_list = []

	def setup(self):
		# clear old lists
		self.entity_list.clear()
		self.tile_list.clear()
		self.zone_list.clear()

		# Set up the villager and add it to the unit_list.
		# self.map = Map(self.tile_list, self.zone_list, DEFAULT_MAP_SIZE)
		use_default = False
		if use_default:
			self.map = Map(self.tile_list, self.zone_list, DEFAULT_MAP_SIZE)
		else:
			self.map = Map(self.tile_list, self.zone_list, DEFAULT_MAP_SIZE, process_array(perlin_array(seed=69)))
		unit0 = Villager(Vector(100, 100))
		unit1 = Villager(Vector(50, 50))
		unit2 = Villager(grid_pos_to_iso(Vector(3, 2)) + Vector(0, TILE_HEIGHT_HALF))
		self.unit_list.append(unit0)
		self.unit_list.append(unit1)
		self.unit_list.append(unit2)

		#military
		militia = Militia(grid_pos_to_iso(Vector(10, 2)) + Vector(0, TILE_HEIGHT_HALF))
		self.unit_list.append(militia)
		archer = Archer(grid_pos_to_iso(Vector(13, 2)) + Vector(0, TILE_HEIGHT_HALF))
		self.unit_list.append(archer)
		knight = Knight(grid_pos_to_iso(Vector(16, 2)) + Vector(0, TILE_HEIGHT_HALF))
		self.unit_list.append(knight)

		## @tidalwaave : 18/11, 22H30
		# tCent = TownCenter(10, 10)
		# self.zoneLayerList.append(tCent)

	def discard_entity(self, dead_entity):
		if isinstance(dead_entity, Unit) and dead_entity in self.unit_list:
			self.unit_list.remove(dead_entity)
		elif isinstance(dead_entity, Zone) and dead_entity in self.zone_list:
			self.zone_list.remove(dead_entity)

	def add_entity(self, new_entity):
		if isinstance(new_entity, Unit) and new_entity not in self.unit_list:
			self.unit_list.append(new_entity)
		elif isinstance(new_entity, Zone) and new_entity not in self.zone_list:
			self.zone_list.append(new_entity)

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

		self.unit_sprite_list = arcade.SpriteList()
		self.tile_sprite_list = arcade.SpriteList()
		self.zone_sprite_list = arcade.SpriteList()

  def setup(self):

		# Variables that will hold sprite lists
		#for e in self.game.game_model.unit_list:
		#	self.unit_sprite_list.append(e.sprite)
		#for t in self.game.game_model.tile_list:
		#	self.tile_sprite_list.append(t.sprite)
		#for z in self.game.game_model.zone_list:
		#	self.zone_sprite_list.append(z.sprite)

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
    
	def setup(self) :
		#clear old lists
		self.entity_sprite_list = arcade.SpriteList()
		self.tile_sprite_list = arcade.SpriteList()
		self.zone_sprite_list = arcade.SpriteList()
		# a UIManager to handle the UI.
		self.manager = arcade.gui.UIManager()

		#Boolean qui indique si le gui dynamic est active ou non
		self.boolean_dynamic_gui = False

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
				anchor_x="center",
				align_x= 200,
				anchor_y="bottom",
				align_y=15,
				child=self.v_box5
			)
		)

		# Create a box for the button in the precedent box, maybe redondant
		self.v_box6 = arcade.gui.UIBoxLayout()
		self.manager.add(
			arcade.gui.UIAnchorWidget(
				anchor_x="center",
				align_x= 400,
				anchor_y="bottom",
				align_y=15,
				child=self.v_box6
			)
		)


	def init_cheats(self) :
		self.display_cheat_input = False

		cheat_list_display = ['NINJALUI', 'BIGDADDY', 'STEROIDS', 'REVEAL MAP', 'NO FOG']

		width = self.game.window.width  # arbitrary
		height = self.game.window.height / 22 # arbitrary
		bg_text = arcade.load_texture("Ressources/img/dark_fond.jpg")
		self.cheat_pane = arcade.gui.UITexturePane(
			CheatsInput(
				x=0,
				y=(self.game.window.height - height) / 2, # middle
				text=f"Enter a cheatcode among {cheat_list_display}", width=width, height=height,
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

		# --- Object sprite lists : Tiles, Zones & Entities
		self.tile_sprite_list.draw()

		for i in self.zone_sprite_list:
			i.draw()
			self.draw_iso_position(i.entity.iso_position)

		for i in self.unit_sprite_list:
			if i.entity.selected:
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
		self.addSaveButton()

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
		self.coord_label.fit_content()


	def addSaveButton(self):
		buttonsize = self.game.window.width / 6
		self.v_box = arcade.gui.UIBoxLayout()
		save_button = SaveButton(self.game.game_model.unit_list, self.game.game_model.tile_list ,self.game.game_model.zone_list, text="Save Game", width=buttonsize)
		self.v_box.add(save_button)
		self.manager.add(
			arcade.gui.UIAnchorWidget(
				anchor_x = "right",
				anchor_y = "bottom",
				child = self.v_box
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
		mouse_position_in_game = Vector(x + self.camera.position.x, y + self.camera.position.y)
		if self.minimap.is_on_minimap_sprite(x, y) :
			self.camera_x = (x * DEFAULT_MAP_SIZE * TILE_WIDTH / self.minimap.size[0]) - ((DEFAULT_MAP_SIZE * TILE_WIDTH) / 2) - self.camera.viewport_width / 2
			self.camera_y = (y * DEFAULT_MAP_SIZE * TILE_HEIGHT / self.minimap.size[1]) - self.camera.viewport_height / 2
			self.camera.move_to([self.camera_x, self.camera_y], 1)
		#Empeche la deselection des entites quand on clique sur le gui static correspondant OR sur option (les valeurs sont dependantes de la taille du button)
		elif (self.boolean_dynamic_gui and (x > self.game.window.width/2 and y < 5*self.HEIGHT_LABEL)) or ( x > self.game.window.width*(5/6) and y > (self.game.window.height - 50)) :
			pass
		elif button == arcade.MOUSE_BUTTON_LEFT:
			self.game.game_controller.select(arcade.get_sprites_at_point(tuple(mouse_position_in_game), self.unit_sprite_list))

		elif button == arcade.MOUSE_BUTTON_RIGHT:
			units_at_point = arcade.get_sprites_at_point(tuple(mouse_position_in_game), self.unit_sprite_list)
			if units_at_point:
				print("unit!")
			else:
				self.game.game_controller.move_selection(mouse_position_in_game)

		elif button == arcade.MOUSE_BUTTON_MIDDLE:
			print(f"position de la souris : {mouse_position_in_game}")
			print(f"position sur la grille : {iso_to_grid_pos(mouse_position_in_game)}")
			pos = mouse_position_in_game
			grid_x = (pos.x / TILE_WIDTH_HALF + pos.y / TILE_HEIGHT_HALF) / 2
			grid_y = (pos.y / TILE_HEIGHT_HALF - (pos.x / TILE_WIDTH_HALF)) / 2
			print(f"position sur la grille sans arrondi : {Vector(grid_x, grid_y)}")

	def on_key_press(self, symbol, modifier):
    mouse_position_in_game = Vector(self.mouse_x + self.camera.position.x, self.mouse_y + self.camera.position.y)
		if symbol == arcade.key.T:  # Faire apparaitre un bâtiment (Town Center pour l'instant...)
			grid_pos = iso_to_grid_pos(mouse_position_in_game)
			tCent = TownCenter(grid_pos)
			self.game.game_controller.add_entity_to_game(tCent)
		elif symbol == arcade.key.F : # cheat window
			self.triggerCheatInput()
		eliif symbol == arcade.key.C:  # Couper arbre
			self.game.game_controller.action_on_zone(mouse_position_in_game)

	def on_mouse_motion(self, x, y, dx, dy):
		"""Called whenever the mouse moves."""
		# Update the coords of the mouse
		self.mouse_x = x
		self.mouse_y = y

	def triggerCheatInput(self) :
		if self.display_cheat_input :
			self.manager.remove(self.cheat_pane)
			self.cheat_pane.child.reset_text()
		else :
			self.manager.add(self.cheat_pane)
		self.display_cheat_input = not self.display_cheat_input

	# test pour les coins mais dois bouger TODO
	def trigger_coin_GUI(self, selected_list) :
		self.v_box4.clear()
		self.v_box5.clear()
		self.v_box6.clear()

		self.boolean_dynamic_gui = False

		if selected_list :
			self.boolean_dynamic_gui = True
			width = self.game.window.width / 2 # other half of the screen
			height = self.minimap.size[1] # same as minimap
			coin_box = arcade.gui.UITextArea(text="Coin I Chiwa", width=width, height=height)
			self.v_box4.add(coin_box.with_space_around(0, 0, 0, 0, arcade.color.BRONZE))

			# Button for coin, you wan click on it but unfortunately, it will unselect the coin which result in the disapearance of the button
			coin_button = arcade.gui.UIFlatButton(text = "Machala",height = 70, width=110)
			self.v_box5.add(coin_button.with_space_around(15,15,15,15,arcade.color.BRONZE))

			coin_button2 = arcade.gui.UIFlatButton(text = "Attaquer", height = 70, width = 110)
			self.v_box5.add(coin_button2.with_space_around(15,15,15,15,arcade.color.BRONZE))

			coin_button3 = ConstructButton(image="map/Tower.png",construct=None)
			self.v_box6.add(coin_button3.with_space_around(15,15,15,15,arcade.color.BRONZE))

	def on_hide_view(self) :
		self.manager.disable()
	
	def discard_sprite(self, dead_sprite):
		if isinstance(dead_sprite.entity, Unit) and dead_sprite in self.unit_sprite_list:
			self.unit_sprite_list.remove(dead_sprite)
		elif isinstance(dead_sprite.entity, Zone) and dead_sprite in self.zone_sprite_list:
			self.zone_sprite_list.remove(dead_sprite)

	def add_sprite(self, new_sprite):
		if isinstance(new_sprite.entity, Unit) and new_sprite not in self.unit_sprite_list:
			self.unit_sprite_list.append(new_sprite)
		elif isinstance(new_sprite.entity, Zone) and new_sprite not in self.zone_sprite_list:
			self.zone_sprite_list.append(new_sprite)
	


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

		# @tidalwaave, 19/12, 23h50 : Time to replace the movements methods, fit 'em in tiles
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
			if isinstance(entity.aimed_entity, Zone):
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
					entity.aimed_entity = z
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
				entity.resource[Res[type(aimed_entity).__name__.upper()]] = harvested
				print(entity.resource)
				entity.aimed_entity = None
				self.dead_entities.add(aimed_entity)


# Main function to launch the game
def main():
	""" Main method """
	game = AoCE()
	arcade.run()

if __name__ == "__main__":  # Python syntax that means "if you are launching from this file, run main()", useful if this file is going to be imported.
	main()
