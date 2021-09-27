""" Example for AoE-like movements """

import arcade
import math

# --- Constants ---
SPRITE_SCALING_COIN = 0.2
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


def isalmost(n, m, d=5):
    """Tests if n and m are close with a maximum distance of d"""
    return abs(n - m) < d


class MyGame(arcade.Window):

    def __init__(self):
        """ Initializer """
        # Call the initializer of arcade.Window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Age Of Cheap Empires TEST")

        # Selection (will be a Villager: an arcade.Sprite)
        self.selection = None

        # Variables that will hold sprite lists
        self.villager_list = None

        # Show the mouse cursor
        self.set_mouse_visible(True)

        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite list
        self.villager_list = arcade.SpriteList()

        # Set up the villager
        self.villager = DummyVillager(50, 50)
        self.villager_list.append(self.villager)

        # Here we use the Simple Physics Engine, maybe we will change this later
        self.physics_engine = arcade.PhysicsEngineSimple(self.villager, arcade.SpriteList())

    def on_draw(self):
        """ Draw everything """
        arcade.start_render()
        self.villager_list.draw()

        # Put the text on the screen.
        output = "Hello World!"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

    def on_update(self, delta_time):
        """ Movement and game logic """
        if self.selection:
            self.selection.update()
        self.physics_engine.update()

    def on_mouse_motion(self, x, y, dx, dy):
        """ Handle Mouse Motion """
        # May be useful to move the camera later. Keep in mind that this function is executed a lot of time per second when you move the mouse.
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        villagers = arcade.get_sprites_at_point((x, y), self.villager_list)

        if self.selection:
            self.selection.move_towards(x, y)
            print(x, y)

        if villagers:
            self.selection = villagers[0]  # ou -1, jsp encore si c'est celui qui est tout derrière ou celui qui est tout devant là.


class DummyVillager(arcade.Sprite):
    """Classe correspondant aux villageois, à fusionner avec la vraie classe correspondant aux villageois"""

    def __init__(self, x, y):
        # coin image from kenney.nl
        self.image = "test_arcadelibrary/coin_01.png"
        super().__init__(self.image, SPRITE_SCALING_COIN, hit_box_algorithm="None")  # Associe un sprite au personnage. Le hit_box_algorithm à non c'est pour éviter
        self.center_x = x  # Initial x coordinate
        self.center_y = y  # Initial y coordinate
        self.aim_x = 0  # x coordinate aimed by the user when he clicked
        self.aim_y = 0  # y coordinate aimed by the user when he clicked
        self.isMoving = False  # Verify if the villager is moving
        self.speed = 3  # Speed of the villager (should probably be a constant)

    def update(self):
        if self.isMoving:
            if isalmost(self.center_x, self.aim_x, 3):
                self.change_x = 0
            if isalmost(self.center_y, self.aim_y, 3):
                self.change_y = 0

    def move_towards(self, x, y):
        distance = math.dist((x, y), (self.center_x, self.center_y))
        self.change_x = self.speed * (x - self.center_x) / distance
        self.change_y = self.speed * (y - self.center_y) / distance
        self.isMoving = True
        self.aim_x = x
        self.aim_y = y


def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
