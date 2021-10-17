import arcade

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 768
SCREEN_TITLE = "Display Test (by Thomas)"
CHARACTER_SCALING = 1
TILE_SCALING = 1
TILE_SIZE = 64
OFFSET = 4*SCREEN_WIDTH//3
def cart_to_iso(x, y):
        iso_x = x - y
        iso_y = (x + y)/2
        return iso_x, iso_y
class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.camera = None
        self.mouse_x = None
        self.mouse_y = None
        self.set_mouse_visible(False)

        arcade.set_background_color(arcade.csscolor.YELLOW_GREEN)

    def on_mouse_motion(self, x, y, dx, dy):
        """
        Called whenever the mouse moves.
        """
        self.x = x
        self.y = y
        self.camera.move_to([self.x,self.y])


    def cart_to_iso(x, y):
        iso_x = x - y
        iso_y = (x + y)/2
        return iso_x, iso_y

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        self.ground_list = arcade.SpriteList(use_spatial_hash=True)
        self.camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
    
        for x in range(0 + OFFSET, SCREEN_WIDTH + OFFSET, 40):
            for y in range(0, SCREEN_WIDTH, 40):
                isox, isoy = cart_to_iso(x,y)
                ground = arcade.Sprite("./map/Tiles/Tiles/ts_grass0/straight/225/0.png", TILE_SCALING)
                ground.center_x = isox
                ground.center_y = isoy
                self.ground_list.append(ground)
        pass
    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_x = x
        self.mouse_y = y
        self.camera.move_to([self.mouse_x,self.mouse_y])
    def on_draw(self):
        """Render the screen."""
        self.camera.use()
        self.clear()
        arcade.start_render()
        self.ground_list.draw()
        # Code to draw the screen goes here
    # def on_update(self, delta_time):
    #     self.camera.move_to([self.mouse_x,self.mouse_y])
    #     self.camera.update()


def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()