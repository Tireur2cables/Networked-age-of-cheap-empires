""" Sprite Sample Program """

import arcade
import math

# --- Constants ---
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_COIN = 0.2
COIN_COUNT = 50

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

def isalmost(n, m, d=1):
    """Tests if n and m are close with a maximum distance of d"""
    return abs(n - m) < d

class MyGame(arcade.Window):
    """ Our custom Window Class"""

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Age Of Cheap Empires TEST")

        # Variables that will hold sprite lists
        self.coin_list = None

        # Set up the player info
        self.coin_sprite = None
        self.selection = None

        self.scene = None
        self.physics_engine = None

        # Show the mouse cursor
        self.set_mouse_visible(True)

        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.coin_list = arcade.SpriteList()

        # Set up the player
        # Character image from kenney.nl
        self.coin_sprite = arcade.Sprite("coin_01.png", SPRITE_SCALING_COIN)
        self.coin_sprite.center_x = 50
        self.coin_sprite.center_y = 50
        self.coin_list.append(self.coin_sprite)

        self.scene = arcade.Scene()
        self.scene.add_sprite("Characters", self.coin_sprite)
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.coin_sprite, self.scene.get_sprite_list("Characters")
        )

    def on_draw(self):
        """ Draw everything """
        arcade.start_render()
        self.coin_list.draw()

        # Put the text on the screen.
        output = "Hello World!"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

    def on_update(self, delta_time):
        self.physics_engine.update()

    def on_mouse_motion(self, x, y, dx, dy):
        """ Handle Mouse Motion """
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        coins = arcade.get_sprites_at_point((x, y), self.coin_list)

        if self.selection:
            print(self.selection.center_x, self.selection.center_y)
            speed = 3
            self.selection.change_x = speed * (x - self.selection.center_x) / math.sqrt((x - self.selection.center_x)**2 + (y - self.selection.center_y)**2)
            self.selection.change_y = speed * (y - self.selection.center_y) / math.sqrt((x - self.selection.center_x)**2 + (y - self.selection.center_y)**2)

        if coins:
            self.selection = coins[0]  # ou -1
            # print(the_coin.change_x)
            # the_coin.center_x += 20
            # the_coin.center_y += 20
            # print(the_coin)



def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
