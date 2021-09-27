import arcade 
import pygame as pg

from map.game import Game
import os

SPRITE_SCALING = 0.5

SCREEN_WIDTH = 1000 
SCREEN_HEIGHT = 800
SCREEN_TITLE = "mapppp"

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
VIEWPORT_MARGIN = 40

MOVEMENT_SPEED = 5


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self):
        """
        Initializer
        """
        # Open a window in full screen mode. Remove fullscreen=True if
        # you don't want to start this way.
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, fullscreen=True)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # This will get the size of the window, and set the viewport to match.
        # So if the window is 1000x1000, then so will our viewport. If
        # you want something different, then use those coordinates instead.
        width, height = self.get_size()
        self.set_viewport(0, width, 0, height)
        arcade.set_background_color(arcade.color.AMAZON)
        self.example_image = arcade.load_texture(":resources:images/tiles/boxCrate_double.png")

    def on_draw(self):
        """
        Render the screen.
        """

        arcade.start_render()

        # Get viewport dimensions
        left, screen_width, bottom, screen_height = self.get_viewport()

        # Draw some boxes on the bottom so we can see how they change
        for x in range(64, 800, 128):
            y = 64
            width = 128
            height = 128
            arcade.isometric_grid_to_screen(x,y,width,height,10,10)
            

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.F10:
            # User hits f. Flip between full and not full screen.
            self.set_fullscreen(not self.fullscreen)

            # Get the window coordinates. Match viewport to window coordinates
            # so there is a one-to-one mapping.
            width, height = self.get_size()
            self.set_viewport(0, width, 0, height)



def main():
    """ Main function """
    MyGame()
    arcade.run()


if __name__ == "__main__":
    main()
