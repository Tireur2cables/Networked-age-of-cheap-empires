# Imports
import arcade
import arcade.gui
from views.CustomButtons import QuitButton

#############################################################
#					MAP VIEW								#
#############################################################

# Constants
CHARACTER_SCALING = 1
TILE_SCALING = 1
TILE_SIZE = 64

CAMERA_MOVE_STEP = 15
CAMERA_MOVE_EDGE = 50

class MapView(arcade.View) :

	def on_show(self) :
		""" This is run once when we switch to this view """

		self.camera = arcade.Camera(self.window.width, self.window.height)
		initial_x, initial_y = self.cart_to_iso(0, 0)		
		self.camera_x = initial_x
		self.camera_y = initial_y

		#coords of the mouse in the middle of the screen by default (and will be update when the mouse will move)
		self.mouse_x = self.window.width/2
		self.mouse_y = self.window.height/2
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

		for x in range(0, self.window.width, 40) :
			for y in range(0, self.window.width, 40) :
				isox, isoy = self.cart_to_iso(x, y)
				ground = arcade.Sprite("./map/Tiles/Tiles/ts_grass0/straight/225/0.png", TILE_SCALING)
				ground.center_x = isox
				ground.center_y = isoy
				self.ground_list.append(ground)

	def addButton(self) :
		# def button size
		buttonsize = self.window.width / 6

		# Create a vertical BoxGroup to align buttons
		self.v_box = arcade.gui.UIBoxLayout()

		# Create the exit button
		quit_button = QuitButton(self.window, text="Quit", width=buttonsize)
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
		if self.mouse_x >= self.window.width - CAMERA_MOVE_EDGE:
			self.camera_x += CAMERA_MOVE_STEP
		elif self.mouse_x <= CAMERA_MOVE_EDGE:
			self.camera_x -= CAMERA_MOVE_STEP
		if self.mouse_y <= CAMERA_MOVE_EDGE:
			self.camera_y -= CAMERA_MOVE_STEP
		elif self.mouse_y >= self.window.height - CAMERA_MOVE_EDGE:
			self.camera_y += CAMERA_MOVE_STEP

	def on_mouse_motion(self, x, y, dx, dy) :
		"""Called whenever the mouse moves."""
		#update the coords of the mouse
		self.mouse_x = x
		self.mouse_y = y

	def on_draw(self):
		"""Render the screen."""
		arcade.start_render()
		self.camera.use()
		self.camera_move()
		self.camera.move_to([self.camera_x, self.camera_y], 0.5)
		self.ground_list.draw()
		self.manager.draw()

	def on_hide_view(self) :
		self.manager.disable()
