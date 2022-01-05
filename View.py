# --- Imports ---
## -- arcade --
import arcade
from arcade.color import BLACK, BROWN_NOSE
import arcade.gui
## -- Others --
from views.CustomButtons import ConstructButton, NextViewButton, ListButton, SaveButton
from map.tileSprite import TileSprite
from map.Minimap import Minimap
from cheats.fonctions import CheatsInput
from utils.vector import Vector
from save.serializationTest import *
from entity.Unit import *
from entity.Zone import *
from utils.isometric import *

# --- Constants ---
CAMERA_MOVE_STEP = 15
CAMERA_MOVE_EDGE = 20
COLOR_STATIC_RESSOURCES = (101, 67, 33, 250)
COLOR_STATIC_RESSOURCES_ICONE = arcade.color.DARK_GRAY


from CONSTANTS import Resource as Res, DEFAULT_MAP_SIZE, TILE_WIDTH, TILE_HEIGHT, TILE_WIDTH_HALF, TILE_HEIGHT_HALF

# --- Image ressources ---
PIC_CIVIL = "./Ressources/img/Population_500x500.png"
PIC_GOLD = "./Ressources/img/Ressources_Or_500x500.png"
PIC_WOOD = "./Ressources/img/Ressources_Wood_500x500.png"
PIC_STONE = "./Ressources/img/Ressources_Pierre_500x500.png"
PIC_FOOD = "./Ressources/img/Ressources_Viandes_500x500.png"

#########################################################################
#							VIEW CLASS									#
#########################################################################

class View():

	def __init__(self, aoce_game):
		""" Initializer """
		self.game = aoce_game

		self.unit_sprite_list = arcade.SpriteList()
		self.tile_sprite_list = arcade.SpriteList()
		self.zone_sprite_list = arcade.SpriteList()

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

		# Sync self.game_model.tile_list with unit_sprite_list
		for e in self.game.game_model.unit_list:
			self.unit_sprite_list.append(e.sprite)
		# Sync self.game_model.tile_list with tile_sprite_list
		for t in self.game.game_model.tile_list:
			self.tile_sprite_list.append(t.sprite)
		# Sync self.game_model.zone_list with zone_sprite_list
		for z in self.game.game_model.zone_list:
			self.zone_sprite_list.append(z.sprite)

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
		self.minimap = Minimap(self, DEFAULT_MAP_SIZE, TILE_WIDTH, TILE_HEIGHT, COLOR_STATIC_RESSOURCES)

		# Create a vertical BoxGroup to align buttons
		self.v_box1 = arcade.gui.UIBoxLayout()

		player_resources = self.game.player.resource
		resources_tab = ["  = 1 ", f" = {player_resources[Res.FOOD]}", f" = {player_resources[Res.WOOD]}", f" = {player_resources[Res.STONE]}", f" = {player_resources[Res.GOLD]}"]

		self.HEIGHT_LABEL = self.minimap.size[1] / len(resources_tab) # in order to have same height as minimap at the end
		self.WIDTH_LABEL = (self.game.window.width / 2) - self.minimap.size[0] - self.HEIGHT_LABEL # moitié - minimap - image

		# Create a text label, contenant le nombre de ressources disponibles pour le joueur
		self.resource_label_list = []
		for val in resources_tab :
			label = arcade.gui.UITextArea(0, 0, self.WIDTH_LABEL, self.HEIGHT_LABEL, val, text_color=(0, 0, 0, 255), font_name=('Impact',))
			self.resource_label_list.append(label)
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

	def update_vbox1(self):
		player_resources = self.game.player.resource
		resources_tab = ["  = 1 ", f" = {player_resources[Res.FOOD]}", f" = {player_resources[Res.WOOD]}", f" = {player_resources[Res.STONE]}", f" = {player_resources[Res.GOLD]}"]
		for label, resource_text in zip(self.resource_label_list, resources_tab):
			label.text = resource_text

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
		self.coord_label.text = f"FPS: {int(arcade.get_fps())} | x = {self.mouse_x}  y = {self.mouse_y}"
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
		save_button = SaveButton(self.game.game_model.unit_list, self.game.game_model.tile_list ,self.game.game_model.zone_list, text="Save Game", width=buttonsize)

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
			self.game.game_controller.select(self.get_closest_sprites(mouse_position_in_game, self.unit_sprite_list))

		elif button == arcade.MOUSE_BUTTON_RIGHT:
			# units_at_point = self.get_closest_sprites(mouse_position_in_game, self.unit_sprite_list)
			# if units_at_point:
			# 	print("unit!")
			# else:
			self.game.game_controller.move_selection(mouse_position_in_game)

		elif button == arcade.MOUSE_BUTTON_MIDDLE:
			print(f"position de la souris : {mouse_position_in_game}")
			print(f"position sur la grille : {iso_to_grid_pos(mouse_position_in_game)}")
			pos = mouse_position_in_game
			grid_x = (pos.x / TILE_WIDTH_HALF + pos.y / TILE_HEIGHT_HALF) / 2
			grid_y = (pos.y / TILE_HEIGHT_HALF - (pos.x / TILE_WIDTH_HALF)) / 2
			print(f"position sur la grille sans arrondi : {Vector(grid_x, grid_y)}")

	def get_closest_sprites(self, mouse_position_in_game, sprite_list):
		sprites_at_point = arcade.get_sprites_at_point(tuple(mouse_position_in_game), sprite_list)
		sprites_at_point_sorted = sorted(sprites_at_point, key=lambda sprite: sprite.center_y)
		return sprites_at_point_sorted

	def on_key_press(self, symbol, modifier):
		mouse_position_in_game = Vector(self.mouse_x + self.camera.position.x, self.mouse_y + self.camera.position.y)
		grid_pos = iso_to_grid_pos(mouse_position_in_game)
		if symbol == arcade.key.T:  # Faire apparaitre un bâtiment (Town Center pour l'instant...)
			tCent = TownCenter(grid_pos)
			self.game.game_controller.add_entity_to_game(tCent)
		elif symbol == arcade.key.F : # cheat window
			self.triggerCheatInput()
		elif symbol == arcade.key.C or symbol == arcade.key.H:  # Couper arbre / Harvest resource
			self.game.game_controller.action_on_zone(self.get_closest_sprites(mouse_position_in_game, self.zone_sprite_list))
		elif symbol == arcade.key.B: # Build something
			self.game.game_controller.build_on_tiles(grid_pos)

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

			coin_button3 = ConstructButton(image="Ressources/img/zones/buildables/Tower.png",construct=None)
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
