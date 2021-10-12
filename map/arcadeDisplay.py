import arcade
from arcade.csscolor import BLACK, GREEN, RED, YELLOW_GREEN 
#import worldConcept.mapMatrix

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Showtime"

class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        pass


    def on_draw(self):
        """Render the screen."""

        arcade.start_render()
        # arcade.draw_polygon_outline(Coordinates(), BLACK, 3)
        arcade.draw_polygon_outline(IsoCoordinates(), RED, 3)
        arcade.draw_polygon_outline(borders(), GREEN, 4)
        # Code to draw the screen goes here
        origin=[0, 0]
        size=8
        cellSize=20
        hw = cellSize*size

        # for colRow in range(1, size):
        #     dim = cellSize*colRow
        #     arcade.draw_line(cartToIso(origin[0]),cartToIso(origin[1] + dim), cartToIso(hw + origin[0]), cartToIso(origin[1] + dim), YELLOW_GREEN, 3)
        #     arcade.draw_line(cartToIso(origin[0] + dim),cartToIso(origin[1]), cartToIso(dim + origin[0]), cartToIso(origin[1] + hw), YELLOW_GREEN, 3)
            
            
                            

def Coordinates(origin=[0, 0], width=100, height=100):
    point_1 = [origin[0], origin[1]]
    point_2 = [origin[0] + height, origin[1]]
    point_3 = [origin[0] + height, origin[1] + width]
    point_4 = [origin[0], origin[1] + width]
    coordinates = [point_1, point_2, point_3, point_4]
    return coordinates

def cartToIso(point):
    isoX = point[0] - point[1]
    isoY = (point[0] + point[1])/2
    return [isoX, isoY]

def IsoCoordinates(origin=[0, 0], width=100, height=100):
    point_1 = [origin[0], origin[1]]
    point_2 = [origin[0] + height, origin[1]]
    point_3 = [origin[0] + height, origin[1] + width]
    point_4 = [origin[0], origin[1] + width]

    # transfo des points en iso
    isoPoint_1 = cartToIso(point_1)
    isoPoint_2 = cartToIso(point_2)
    isoPoint_3 = cartToIso(point_3)
    isoPoint_4 = cartToIso(point_4)
    iso_coordinates = [isoPoint_1, isoPoint_2, isoPoint_3, isoPoint_4]
    return iso_coordinates

def borders(origin=[0, 0], size=8, cellSize=20):
    hw = cellSize*size
    borderPoints = [cartToIso(origin),
                    cartToIso([origin[0], hw + origin[1]]),
                    cartToIso([hw + origin[0], hw + origin[1]]),
                    cartToIso([hw + origin[0], origin[1]])]
    return borderPoints





def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()