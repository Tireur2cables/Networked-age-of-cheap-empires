""" Example for AoE-like movements! """

import arcade
from utils.vector import Vector

# --- Constants ---
SPRITE_SCALING_COIN = 0.2
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


def isalmost(n, m, d=5):
	"""Tests if n and m are close with a maximum distance of d"""
	return abs(n - m) < d


class AoCE(arcade.Window):

	def __init__(self):
		""" Initializer """
		# Call the initializer of arcade.Window
		super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Age Of Cheap Empires TEST")
		self.game_model = Model(self)
		self.game_view = View(self)  # Je ne sais pas comment modifier autrement la valeur de "set_mouse_visible"
		self.game_controller = Controller(self)

		# Variables for communications between model, view and controller.
		self.toDraw = []
		arcade.set_background_color(arcade.color.AMAZON)

	def setup(self):
		""" Set up the game and initialize the variables. (Re-called when we want to restart the game without exiting it)."""
		self.game_model.setup()
		self.game_view.setup()
		self.game_controller.setup()

	def on_update(self, *args):  # Redirecting on_update to the Controller
		self.game_controller.on_update(*args)

	def on_mouse_press(self, *args):  # Redirecting inputs to the controller
		self.game_controller.on_mouse_press(*args)

	def on_draw(self):
		self.game_view.on_draw()


class Model():
	def __init__(self, aoce_game):
		self.game = aoce_game

	def setup(self):
		pass


class View():
	def __init__(self, aoce_game):
		self.game = aoce_game

		# Variables that will hold sprite lists
		self.villager_list = None

		# Show the mouse cursor
		self.game.set_mouse_visible(True)

	def setup(self):
		# Sprite list
		self.villager_list = arcade.SpriteList()

		# Set up the villager
		self.villager = DummyVillager(Vector(50, 50))
		self.villager_list.append(self.villager)

	def on_draw(self):
		""" Draw everything """
		arcade.start_render()
		self.villager_list.draw()

	def get_villager_list(self):
		return self.villager_list


class Controller():
	def __init__(self, aoce_game):
		self.game = aoce_game

		# Selection (will be a Villager: an arcade.Sprite)
		self.selection = []

	def setup(self):
		pass

	def on_update(self, delta_time):
		""" Movement and game logic """
		for i in self.selection:
			i.update()

	def on_mouse_motion(self, x, y, dx, dy):
		""" Handle Mouse Motion """
		# May be useful to move the camera later. Keep in mind that this function is executed a lot of time per second when you move the mouse.
		pass

	def on_mouse_press(self, x, y, button, key_modifiers):
		mouse_position = Vector(x, y)
		villagers = arcade.get_sprites_at_point(tuple(mouse_position), self.game.game_view.get_villager_list())

		for i in self.selection:
			i.move_towards(mouse_position)
			print(mouse_position)

		if villagers:
			self.selection.append(villagers[0])  # ou -1, jsp encore si c'est celui qui est tout derrière ou celui qui est tout devant là.


class DummyVillager(arcade.Sprite):
	"""Classe correspondant aux villageois, à fusionner avec la vraie classe correspondant aux villageois"""

	def __init__(self, pos):
		# coin image from kenney.nl
		self.image = "Movements/coin_01.png"  # This may cause an error depending on how the IDE is configurated. I now how to fix this but haven't implemented it for now.
		super().__init__(self.image, SPRITE_SCALING_COIN, hit_box_algorithm="None")  # Associe un sprite au personnage. Le hit_box_algorithm à non c'est pour éviter
		self.pos = pos
		self.center_x, self.center_y = tuple(self.pos)  # Initial coordinates
		self.aim = Vector(0, 0)  # coordinate aimed by the user when he clicked
		self.change = Vector(0, 0)
		self.isMoving = False  # Verify if the villager is moving
		self.speed = 5  # Speed of the villager (should probably be a constant)

	def update(self):
		print(self.change)
		if self.isMoving:
			if isalmost(self.center_x, self.aim.x, self.speed):
				self.change.x = 0  # If it is close to where it aims, stop moving.
			if isalmost(self.center_y, self.aim.y, self.speed):
				self.change.y = 0
		self.center_x += self.change.x
		self.center_y += self.change.y
		self.pos = Vector(self.center_x, self.center_y)

	def move_towards(self, v):
		# The following calculation is necessary to have uniform speeds :
		self.aim = v
		self.change = self.speed * ((self.aim - self.pos).normalized())
		# We want the same speed no matter what the distance between the villager and where he needs to go is.
		self.isMoving = True


def main():
	""" Main method """
	game = AoCE()
	game.setup()
	arcade.run()
