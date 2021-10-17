# Import
from MyWindow import MyWindow
from MainView import MainView
import arcade

# Launch the game with the main menu
def main():
	""" Main function """
	window = MyWindow()
	start_view = MainView()
	window.show_view(start_view)
	arcade.run()

if __name__ == "__main__":
	main()
