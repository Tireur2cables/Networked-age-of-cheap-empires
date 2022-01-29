# --- Imports ---
## -- arcade --
from turtle import window_height, window_width
import arcade
from arcade.color import BLACK, BROWN_NOSE
import arcade.gui
## -- Others --
from views.CustomButtons import ActionButton, ConstructButton, NextViewButton, ListButton, SaveButton
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
button_texture = "Ressources/img/button_background.png"

# --- Launch setup ---
from LAUNCH_SETUP import LAUNCH_DEBUG_DISPLAY

#########################################################################
#							VIEW CLASS									#
#########################################################################

class View():

# --- Setup ---

	def __init__(self, aoce_game):
		""" Initializer """
		self.game = aoce_game

		self.unit_sprite_list = arcade.SpriteList()
		self.tile_sprite_list = arcade.SpriteList()
		self.zone_sprite_list = arcade.SpriteList()

		self.mode = "move"

		self.resource_label_list = []

	def setup(self) :
		#clear old lists
		self.entity_sprite_list = arcade.SpriteList()
		self.tile_sprite_list = arcade.SpriteList()
		self.zone_sprite_list = arcade.SpriteList()

		#Pour le GUI, les flags indiquant si on veut construire un batiment
		self.reset_construct_flags()

		# a UIManager to handle the UI.
		self.manager = arcade.gui.UIManager()

		#Boolean qui indique si le gui dynamic est active ou non
		self.boolean_dynamic_gui = False

		self.init_dynamic_gui()
		self.init_cheats()

		# Sync self.game_model.tile_list with tile_sprite_list
		for t in self.game.game_model.tile_list:
			self.tile_sprite_list.append(t.sprite)
		# Sync self.game_model.zone_list with zone_sprite_list
		for z in self.game.game_model.zone_list:
			self.zone_sprite_list.append(z.sprite)

	def reset_construct_flags(self) :
		self.HouseRequest = 0
		self.StoragePitRequest = 0
		self.GranaryRequest = 0
		self.BarracksRequest = 0
		self.TownCenterRequest = 0

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

		player = self.game.players["player"]
		player_resources = player.resource
		resources_tab = [f"  = {player.nb_unit}/{player.max_unit} ", f" = {player_resources[Res.FOOD]}", f" = {player_resources[Res.WOOD]}", f" = {player_resources[Res.STONE]}", f" = {player_resources[Res.GOLD]}"]

		self.HEIGHT_LABEL = self.minimap.size[1] / len(resources_tab) # in order to have same height as minimap at the end
		self.WIDTH_LABEL = (self.game.window.width / 2) - self.minimap.size[0] - self.HEIGHT_LABEL # moitié - minimap - image

		# Create a text label, contenant le nombre de ressources disponibles pour le joueur
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



# --- Adding/Discarding Sprites ---

	def add_sprite(self, new_sprite):
		if isinstance(new_sprite.entity, Unit) and new_sprite not in self.unit_sprite_list:
			self.unit_sprite_list.append(new_sprite)
		elif isinstance(new_sprite.entity, Zone) and new_sprite not in self.zone_sprite_list:
			self.zone_sprite_list.append(new_sprite)

	def discard_sprite(self, dead_sprite):
		if isinstance(dead_sprite.entity, Unit) and dead_sprite in self.unit_sprite_list:
			self.unit_sprite_list.remove(dead_sprite)
		elif isinstance(dead_sprite.entity, Zone) and dead_sprite in self.zone_sprite_list:
			self.zone_sprite_list.remove(dead_sprite)



# --- Drawing ---

	def on_draw(self):
		""" Draw everything """
		arcade.start_render()

		# --- Object sprite lists : Tiles, Zones & Entities
		self.tile_sprite_list.draw(pixelated=True)

		for s in self.zone_sprite_list:
			zone = s.entity
			if zone.selected:
				for x in range(zone.tile_size[0]):
					for y in range(zone.tile_size[1]):
						tile_outline = self.get_tile_outline(grid_pos_to_iso(iso_to_grid_pos(zone.iso_position) + Vector(x, y)))
						arcade.draw_polygon_outline(tile_outline, (255, 255, 255))
				nbr_health_bar = 1
				if zone.health > 0:
					self.draw_bar(zone.iso_position, zone.health, zone.max_health, arcade.color.RED)
					nbr_health_bar += 1

				if isinstance(zone, Resources):
					self.draw_bar(zone.iso_position, zone.amount, zone.max_amount, arcade.color.BLUE, nbr_health_bar=nbr_health_bar)
					nbr_health_bar +=1
				elif isinstance(zone, TownCenter) and zone.is_producing:
					self.draw_bar(zone.iso_position, int(zone.action_timer), int(zone.villager_cooldown), arcade.color.GREEN, nbr_health_bar=nbr_health_bar)
					nbr_health_bar +=1
			s.draw(pixelated=True)

			if LAUNCH_DEBUG_DISPLAY:
				self.draw_iso_position(s.entity.iso_position)

		for s in self.unit_sprite_list:
			entity = s.entity
			if entity.selected :
				s.draw_hit_box((255, 0, 0), line_thickness=3)
				map_position = iso_to_grid_pos(entity.iso_position)
				# tile_below = self.game.game_model.map.get_tile_at(map_position)
				tile_outline = self.get_tile_outline(grid_pos_to_iso(map_position))
				arcade.draw_polygon_outline(tile_outline, (255, 255, 255))
				# tile_below.sprite.draw_hit_box((255, 0, 0), line_thickness=3)
				self.draw_bar(entity.iso_position, entity.health, entity.max_health, arcade.color.RED)
				if entity.is_interacting and (aimed_entity := entity.aimed_entity):
					if isinstance(aimed_entity, Resources):
						self.draw_bar(aimed_entity.iso_position, aimed_entity.health, aimed_entity.max_health, arcade.color.RED)
						self.draw_bar(aimed_entity.iso_position, aimed_entity.amount, aimed_entity.max_amount, arcade.color.BLUE,nbr_health_bar=2)
					elif isinstance(aimed_entity, WorkSite):
						self.draw_bar(entity.iso_position, int(entity.action_timer), aimed_entity.zone_to_build.build_time, arcade.color.GREEN, nbr_health_bar=2)
			s.draw(pixelated=True)

			if LAUNCH_DEBUG_DISPLAY:
				self.draw_iso_position(entity.iso_position)

		if LAUNCH_DEBUG_DISPLAY:
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



# --- View & Camera ---

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

		arcade.set_background_color(arcade.csscolor.BLACK)

		self.manager.enable()

		self.static_menu()
		self.addButton()
		self.addCoordLabel()

	def on_hide_view(self) :
		self.manager.disable()

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



# --- Inputs ---

	def on_mouse_motion(self, x, y, dx, dy):
		"""Called whenever the mouse moves."""
		# Update the coords of the mouse
		self.mouse_x = x
		self.mouse_y = y

	def on_mouse_press(self, x, y, button, key_modifiers) :
		mouse_position_in_game = Vector(x + self.camera.position.x, y + self.camera.position.y)
		if self.minimap.is_on_minimap_sprite(x, y) :
			self.camera_x = (x * DEFAULT_MAP_SIZE * TILE_WIDTH / self.minimap.size[0]) - ((DEFAULT_MAP_SIZE * TILE_WIDTH) / 2) - self.camera.viewport_width / 2
			self.camera_y = (y * DEFAULT_MAP_SIZE * TILE_HEIGHT / self.minimap.size[1]) - self.camera.viewport_height / 2
			self.camera.move_to([self.camera_x, self.camera_y], 1)
		#Empeche la deselection des entites quand on clique sur le gui static correspondant OR sur option (les valeurs sont dependantes de la taille du button)
		elif (self.boolean_dynamic_gui and (x > self.game.window.width/2 and y < 5*self.HEIGHT_LABEL)) or ( x > self.game.window.width*(5/6) and y > (self.game.window.height - self.game.window.height/10)) :
			pass
		elif button == arcade.MOUSE_BUTTON_LEFT :
			#Si le bouton maisno a ete selectionne, la prochaine fois qu on click gauche, le villageois constuira une maison.
			if self.HouseRequest == 1 :
				self.game.game_controller.human_order_towards_position("build", "player", mouse_position_in_game, "House")
				self.HouseRequest = 0
			elif self.StoragePitRequest == 1 :
				self.game.game_controller.human_order_towards_position("build", "player", mouse_position_in_game, "StoragePit")
				self.StoragePitRequest = 0
			elif self.GranaryRequest == 1 :
				self.game.game_controller.human_order_towards_position("build", "player", mouse_position_in_game, "Granary")
				self.GranaryRequest = 0
			elif self.BarracksRequest == 1 :
				self.game.game_controller.human_order_towards_position("build", "player", mouse_position_in_game, "Barracks")
				self.BarracksRequest = 0
			elif self.TownCenterRequest == 1 :
				self.game.game_controller.human_order_towards_position("build", "player", mouse_position_in_game, "TownCenter")
				self.TownCenterRequest = 0
			else:
				closest_unit_sprites = self.get_closest_sprites(mouse_position_in_game, self.unit_sprite_list)
				if closest_unit_sprites:
					self.game.game_controller.select("player", closest_unit_sprites)
				else:
					closest_zone_sprites = self.get_closest_sprites(mouse_position_in_game, self.zone_sprite_list)
					if closest_zone_sprites:
						self.game.game_controller.select_zone("player", closest_zone_sprites)
					else:
						self.game.game_controller.clear_faction_selection("player")
				# draw interactive ui of selected
				self.trigger_Villager_GUI(self.game.game_controller.selection)

		elif button == arcade.MOUSE_BUTTON_RIGHT :
			self.reset_construct_flags() # permet d'annuler une construction
			units_at_point = self.get_closest_sprites(mouse_position_in_game, self.unit_sprite_list)
			zones_at_point = self.get_closest_sprites(mouse_position_in_game, self.zone_sprite_list)
			if zones_at_point:
				self.game.game_controller.human_order_towards_sprites("stock", "player", zones_at_point)
				# TODO ici, reparer le batiment s'il est abimé et que on a pas de ressources a deposer et batiment a nous
			else:
				self.game.game_controller.human_order_towards_position("move", "player", mouse_position_in_game)
			# TODO ici attquer si batiment ou unité pas a nous

		elif button == arcade.MOUSE_BUTTON_MIDDLE:
			print(f"position de la souris : {mouse_position_in_game}")
			print(f"position sur la grille : {iso_to_grid_pos(mouse_position_in_game)}")
			pos = mouse_position_in_game
			grid_x = (pos.x / TILE_WIDTH_HALF + pos.y / TILE_HEIGHT_HALF) / 2
			grid_y = (pos.y / TILE_HEIGHT_HALF - (pos.x / TILE_WIDTH_HALF)) / 2
			print(f"position sur la grille sans arrondi : {Vector(grid_x, grid_y)}")

	def on_key_press(self, symbol, modifier):
		mouse_position_in_game = Vector(self.mouse_x + self.camera.position.x, self.mouse_y + self.camera.position.y)
		if self.game.game_controller.unit_in_selection("player"):
			if self.mode == "move":
				if symbol == arcade.key.F: # cheat window
					self.triggerCheatInput()
				elif symbol == arcade.key.C or symbol == arcade.key.H:  # Couper arbre / Harvest resource
					self.game.game_controller.human_order_towards_sprites("harvest", "player", self.get_closest_sprites(mouse_position_in_game, self.zone_sprite_list))
				elif symbol == arcade.key.B:
					self.mode = "build"
					print("build mode!")
			elif self.mode == "build":
				if symbol == arcade.key.H: # Build something
					self.game.game_controller.human_order_towards_position("build", "player", mouse_position_in_game, "House")
				elif symbol == arcade.key.S:
					self.game.game_controller.human_order_towards_position("build", "player", mouse_position_in_game, "StoragePit")
				elif symbol == arcade.key.G:
					self.game.game_controller.human_order_towards_position("build", "player", mouse_position_in_game, "Granary")
				elif symbol == arcade.key.B:
					self.game.game_controller.human_order_towards_position("build", "player", mouse_position_in_game, "Barracks")
				# elif symbol == arcade.key.D:
				# 	self.game.game_controller.human_order_towards_position("build", "player", mouse_position_in_game, "Dock")
				self.mode = "move"
				print("move mode!")
		else:
			if symbol == arcade.key.V:
				self.game.game_controller.human_order_with_zone("populate", "player")

	def get_closest_sprites(self, mouse_position_in_game, sprite_list):
		sprites_at_point = arcade.get_sprites_at_point(tuple(mouse_position_in_game), sprite_list)
		sprites_at_point_sorted = sorted(sprites_at_point, key=lambda sprite: sprite.center_y)
		return sprites_at_point_sorted



# --- GUI ---

	def triggerCheatInput(self) :
		if self.display_cheat_input :
			self.manager.remove(self.cheat_pane)
			self.cheat_pane.child.reset_text()
		else :
			self.manager.add(self.cheat_pane)
		self.display_cheat_input = not self.display_cheat_input

	def draw_bar(self, pos, health, max_health, color, nbr_health_bar=1):
		if max_health:
			y_offset = 10
			arcade.draw_rectangle_filled(pos.x, pos.y - nbr_health_bar*y_offset, 36, 12, arcade.color.GRAY)
			if health > 0:
				arcade.draw_rectangle_filled(pos.x - (32//2)*(1 - health/max_health), pos.y - nbr_health_bar*y_offset, (health*32)/max_health, 8, color)

	def init_dynamic_gui(self) :
		# Create a box group to align the 'open' button in the center
		# Box pour le UITextArea qui contiens les stats du personnage
		self.v_box4 = arcade.gui.UIBoxLayout()
		self.manager.add(
			arcade.gui.UIAnchorWidget(
				anchor_x="right",
				align_x= - self.game.window.width / 3,
				anchor_y="bottom",
				child=self.v_box4
			)
		)

		# Box pour le UITextArea qui contiens les actions du personnage
		self.v_box7 = arcade.gui.UIBoxLayout()
		self.manager.add(
			arcade.gui.UIAnchorWidget(
				anchor_x="right",
				anchor_y="bottom",
				child=self.v_box7
			)
		)

		# Create a box for the batiment buildable by villagers
		self.v_box5 = arcade.gui.UIBoxLayout()
		self.manager.add(
			arcade.gui.UIAnchorWidget(
				anchor_x="right",
				align_x=-self.game.window.width / 3 + self.game.window.width / 12 + (self.game.window.width / 3 - self.game.window.width / 6) / 3,
				anchor_y="bottom",
				align_y=(self.game.window.height / 4 - self.game.window.height * 3 / 12) / 2,
				child=self.v_box5
			)
		)

		# Create a box for the batiment buildable by villagers
		self.v_box9 = arcade.gui.UIBoxLayout()
		self.manager.add(
			arcade.gui.UIAnchorWidget(
				anchor_x="right",
				align_x=-self.game.window.width / 3 + self.game.window.width / 6 + (self.game.window.width / 3 - self.game.window.width / 6) * 2 / 3,
				anchor_y="bottom",
				align_y=(self.game.window.height / 4 - self.game.window.height * 2 / 12) / 2,
				child=self.v_box9
			)
		)



		# Create a box for the button in the precedent box, maybe redondant
		# Heberge la sprite
		self.v_box6 = arcade.gui.UIBoxLayout()
		self.manager.add(
			arcade.gui.UIAnchorWidget(
				anchor_x="center",
				align_x=self.game.window.width / 24 + (self.game.window.width / 6 - self.game.window.width / 12) / 2, # center sprite in rectangle
				anchor_y="bottom",
				align_y=self.game.window.height * 1 / 8 - (self.game.window.height * 2 / 32), # center sprite in rectangle
				child=self.v_box6
			)
		)

		# Heberge l affichage des ressources
		self.v_box8 = arcade.gui.UIBoxLayout(vertical=False)
		self.manager.add(
			arcade.gui.UIAnchorWidget(
				anchor_x="left",
				align_x=self.game.window.width / 2 + (self.game.window.width / 6 - self.game.window.width / 8) / 2,
				anchor_y="bottom",
				align_y=10,
				child=self.v_box8
			)
		)

		# Create a box for the villagers buildable by towncenters
		self.v_box10 = arcade.gui.UIBoxLayout()
		self.manager.add(
			arcade.gui.UIAnchorWidget(
				anchor_x="right",
				align_x=-self.game.window.width / 3 + self.game.window.width / 12 + (self.game.window.width / 3 - self.game.window.width / 12) / 2,
				anchor_y="bottom",
				align_y=(self.game.window.height / 4 - self.game.window.height / 12) / 2,
				child=self.v_box10
			)
		)

		# Create a box for the military buildable by barracks
		self.v_box11 = arcade.gui.UIBoxLayout()
		self.manager.add(
			arcade.gui.UIAnchorWidget(
				anchor_x="right",
				align_x=-self.game.window.width / 3 + self.game.window.width / 12 + (self.game.window.width / 3 - self.game.window.width / 6) / 3,
				anchor_y="bottom",
				align_y=(self.game.window.height / 4 - self.game.window.height * 3 / 12) / 2,
				child=self.v_box11
			)
		)

		# Create a box for the military buildable by barracks
		self.v_box12 = arcade.gui.UIBoxLayout()
		self.manager.add(
			arcade.gui.UIAnchorWidget(
				anchor_x="right",
				align_x=-self.game.window.width / 3 + self.game.window.width / 6 + (self.game.window.width / 3 - self.game.window.width / 6) * 2 / 3,
				anchor_y="bottom",
				align_y=(self.game.window.height / 4 - self.game.window.height * 3 / 12) / 2,
				child=self.v_box12
			)
		)

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

	def update_resources_gui(self):
		player = self.game.players["player"]
		player_resources = player.resource
		resources_tab = [f"  = {player.nb_unit}/{player.max_unit} ", f" = {player_resources[Res.FOOD]}", f" = {player_resources[Res.WOOD]}", f" = {player_resources[Res.STONE]}", f" = {player_resources[Res.GOLD]}"]
		for label, resource_text in zip(self.resource_label_list, resources_tab):
			label.text = resource_text

	def update_villager_resources_gui(self) :
		if self.boolean_dynamic_gui :
			self.trigger_Villager_GUI(self.game.game_controller.selection)

	# test pour les coins mais dois bouger TODO
	def trigger_Villager_GUI(self, selected_list) :
		self.v_box4.clear()
		self.v_box5.clear()
		self.v_box6.clear()
		self.v_box7.clear()
		self.v_box8.clear()
		self.v_box9.clear()
		self.v_box10.clear()
		self.v_box11.clear()
		self.v_box12.clear()

		self.boolean_dynamic_gui = False
		if selected_list["player"] : # someting is selected
			self.boolean_dynamic_gui = True

			width = self.game.window.width / 2 # other half of the screen
			height = self.minimap.size[1] # same as minimap

			for s in selected_list["player"] :
				if isinstance(s, Entity) : # add entiity info
					titre = s.name if s.faction == "None" else s.name + " [" + s.faction + "] "
					entity_box_stat = arcade.gui.UITextArea(text=titre, width=width / 3, height=height)
					self.v_box4.add(entity_box_stat.with_space_around(0, 0, 0, 0, arcade.color.DARK_JUNGLE_GREEN))

					entity_life = arcade.gui.UITextArea(text ="Vie " + str(s.health) + " / " + str(s.max_health), text_color = arcade.color.RED, width=width / 8)
					self.v_box8.add(entity_life.with_border())

					sprite_image = arcade.gui.UITextArea(text="", width=width / 6, height=height / 2)
					self.v_box6.add(sprite_image.with_background(s.sprite.texture))

				if isinstance(s, Resources) : # montre les ressources restantes
					ressources_restantes = arcade.gui.UITextArea(text="Ressources : " + str(s.amount) + " / " + str(s.max_amount), text_color=arcade.color.GREEN, width=width / 8)
					self.v_box8.add(ressources_restantes.with_border())

				elif s.faction == "player" : # ouvre les actions seulement si la selection nnous appartient

					if isinstance(s, Villager) : # add villager options
						villager_ressources = arcade.gui.UITextArea(text="Ressources : " + str(s.nb_resources()), text_color=arcade.color.PINK, width=width / 8)
						self.v_box8.add(villager_ressources.with_border())

						villager_box_action = arcade.gui.UITextArea(text="Actions", width=width * 2 / 3, height=height)
						self.v_box7.add(villager_box_action.with_space_around(0, 0, 0, 0, arcade.color.METALLIC_SEAWEED))

						storagepit_villager = ConstructButton(aoce_game=self.game, image="Ressources/img/zones/buildables/storagepit.png", text="StoragePit", width=width / 6, height=self.game.window.height / 12)
						self.v_box5.add(storagepit_villager.with_background(arcade.load_texture(button_texture)))

						house_villager = ConstructButton(aoce_game=self.game, image="Ressources/img/zones/buildables/house.png", text="House", width=width / 6, height=self.game.window.height / 12)
						self.v_box5.add(house_villager.with_background(arcade.load_texture(button_texture)))

						granary_villager = ConstructButton(aoce_game=self.game, image="Ressources/img/zones/buildables/granary.png", text="Granary", width=width / 6, height=self.game.window.height / 12)
						self.v_box5.add(granary_villager.with_background(arcade.load_texture(button_texture)))

						barracks_villager = ConstructButton(aoce_game=self.game, image="Ressources/img/zones/buildables/barracks.png", text="Barracks", width=width / 6, height=self.game.window.height / 12)
						self.v_box9.add(barracks_villager.with_background(arcade.load_texture(button_texture)))

						towncenter_villager = ConstructButton(aoce_game=self.game, image="Ressources/img/zones/buildables/towncenter.png", text="TownCenter", width=width / 6, height=self.game.window.height / 12)
						self.v_box9.add(towncenter_villager.with_background(arcade.load_texture(button_texture)))



					elif isinstance(s, Zone) : # batiment du joueur
						if not isinstance(s, House) : # ne pas l'afficher sur les batiments qui ne possèdent aucune action
							villager_box_action = arcade.gui.UITextArea(text="Actions", width=width * 2 / 3, height=height)
							self.v_box7.add(villager_box_action.with_space_around(0, 0, 0, 0, arcade.color.METALLIC_SEAWEED))

						if isinstance(s, TownCenter) :
							villager_button = ActionButton(text="Villageois", width=width / 6, height=self.game.window.height / 12, batiment=s, image="Ressources/img/units/villager_stand.png", aoce_game=self.game)
							self.v_box10.add(villager_button.with_background(arcade.load_texture(button_texture)))

						elif isinstance(s, Barracks) :
							militia_button = ActionButton(text="Milice", width=width / 6, height=self.game.window.height / 12, batiment=s, image="Ressources/img/units/militia_stand.png", aoce_game=self.game)
							self.v_box11.add(militia_button.with_background(arcade.load_texture(button_texture)))

							spearman_button = ActionButton(text="Lancier", width=width / 6, height=self.game.window.height / 12, batiment=s, image="Ressources/img/units/spearman_stand.png", aoce_game=self.game)
							self.v_box11.add(spearman_button.with_background(arcade.load_texture(button_texture)))

							archer_button = ActionButton(text="Archer", width=width / 6, height=self.game.window.height / 12, batiment=s, image="Ressources/img/units/archer_stand.png", aoce_game=self.game)
							self.v_box11.add(archer_button.with_background(arcade.load_texture(button_texture)))

							skirmisher_button = ActionButton(text="Escarmoucheur", width=width / 6, height=self.game.window.height / 12, batiment=s, image="Ressources/img/units/skirmisher_stand.png", aoce_game=self.game)
							self.v_box12.add(skirmisher_button.with_background(arcade.load_texture(button_texture)))

							scout_button = ActionButton(text="Eclaireur", width=width / 6, height=self.game.window.height / 12, batiment=s, image="Ressources/img/units/scoutcavalry_stand.png", aoce_game=self.game)
							self.v_box12.add(scout_button.with_background(arcade.load_texture(button_texture)))

							knight_button = ActionButton(text="Chevalier", width=width / 6, height=self.game.window.height / 12, batiment=s, image="Ressources/img/units/knight_stand.png", aoce_game=self.game)
							self.v_box12.add(knight_button.with_background(arcade.load_texture(button_texture)))



				break # ce break sera a enlever si on gere la selection multiple
