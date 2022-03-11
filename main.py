# Launch your code from here
# Import the module you want to launch
# Example : import objects.Entity to launch Entity.py locatated in the objects directory.
import game
import sys

if __name__ == "__main__":  # Python syntax that means "if you are launching from this file, run main()", useful if this file is going to be imported.
	print(str(sys.argv))
	game.main()
