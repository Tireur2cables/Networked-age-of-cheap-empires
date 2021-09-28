""" Example for AoE-like movements! """

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

    def on_draw(self):
        """ Draw everything """
        arcade.start_render()
        self.villager_list.draw()

    def on_update(self, delta_time):
        """ Movement and game logic """
        if self.selection:
            self.selection.update()

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
        self.image = "Movements/coin_01.png"  # This may cause an error depending on how the IDE is configurated. I now how to fix this but haven't implemented it for now.
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
                self.change_x = 0  # If it is close to where it aims, stop moving.
            if isalmost(self.center_y, self.aim_y, 3):
                self.change_y = 0
        self.center_x += self.change_x
        self.center_y += self.change_y

    def move_towards(self, x, y):
        distance = math.dist((x, y), (self.center_x, self.center_y))
        # The following calculation is necessary to have uniform speeds :
        # We want the same speed no matter what the distance between the villager and where he needs to go is.
        self.change_x = self.speed * (x - self.center_x) / distance  # Creates the x coordinate of a unit vector. Then we multiply it by the speed.
        self.change_y = self.speed * (y - self.center_y) / distance  # Creates the y coordinate of a unit vector. Then we multiply it by the speed.
        self.isMoving = True
        self.aim_x = x
        self.aim_y = y


def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":  # Python syntax that means "if you are launching from this file, run main()", useful if this file is going to be imported.
    main()
