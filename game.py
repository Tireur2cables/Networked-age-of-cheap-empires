import arcade
from utils.vector import Vector
from objects.Entity import Entity
from objects.EntitySprite import EntitySprite

# --- Constants ---
SPRITE_SCALING_COIN = 0.2
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


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
		self.entity_list = []

	def setup(self):
		# Set up the villager and add it to the entity_list.
		self.entity_list.append(Entity(Vector(50, 50), 10, 10))


class View():

	def __init__(self, aoce_game):
		self.game = aoce_game

		# Variables that will hold sprite lists
		self.sprite_list = arcade.SpriteList()

		# Show the mouse cursor
		self.game.set_mouse_visible(True)

	def setup(self):
		for index, item in enumerate(self.game.game_model.entity_list):
			# coin image from kenney.nl
			self.sprite_list.append(EntitySprite(index, item, "Movements/coin_01.png", SPRITE_SCALING_COIN, center_x=item.position.x, center_y=item.position.y, hit_box_algorithm="None"))
		# La ligne d'au dessus créer un sprite associé au personnage et le met dans une liste. Le hit_box_algorithm à non c'est pour éviter d'utiliser une hitbox complexe, inutile pour notre projet.
		# "Movements/coin_01.png" may cause an error depending on how the IDE is configurated (what is the root directory). I now how to fix this but haven't implemented it for now.

	def on_draw(self):
		""" Draw everything """
		arcade.start_render()
		self.sprite_list.draw()

	def get_sprite_list(self):
		return self.sprite_list


class Controller():
	def __init__(self, aoce_game):
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

	def on_mouse_motion(self, x, y, dx, dy):
		""" Handle Mouse Motion """
		# May be useful to move the camera later. Keep in mind that this function is executed a lot of time per second when you move the mouse.
		pass

	def on_mouse_press(self, x, y, button, key_modifiers):
		if button == arcade.MOUSE_BUTTON_LEFT:
			mouse_position = Vector(x, y)
			villagers = arcade.get_sprites_at_point(tuple(mouse_position), self.game.game_view.get_sprite_list())


			for i in self.selection:
				i.entity.aim_towards(mouse_position)
				print(mouse_position)

			if villagers:
				self.selection.append(villagers[0])  # ou -1, jsp encore si c'est celui qui est tout derrière ou celui qui est tout devant là.


def main():
	""" Main method """
	game = AoCE()
	game.setup()
	arcade.run()
