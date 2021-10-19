# --- Imports ---
import arcade
from utils.vector import Vector
from objects.Unit import Unit
from objects.EntitySprite import EntitySprite
from views.MainView import MainView

# --- Constants ---
SPRITE_SCALING_COIN = 0.2
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Age Of Cheap Empire"
MUSIC = "./Ressources/music/logon_aoe_music3s.wav"

#########################################################################
#							MAIN CLASS									#
#########################################################################

class AoCE(arcade.Window) :

	def __init__(self) :
		""" Initializer """
		# Call the initializer of arcade.Window
		super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=False, fullscreen=True)
		#arcade.set_background_color(arcade.csscolor.WHITE)

		# Show the mouse cursor
		self.set_mouse_visible(True)

		# Lance la musique
		self.my_music = arcade.load_sound(MUSIC, streaming=True)
		self.media_player = self.my_music.play(loop=True)

		# # Variables for communications between model, view and controller.
		# self.toDraw = []

	def on_show(self) :
		# Affiche le main menu
		start_view = MainView()
		self.show_view(start_view)

	# Stop all process and exit arcade
	def exit(self) :
		self.media_player.delete()
		arcade.exit()

	# Set fulllscreen or defaults : SCREEN_WIDTH x SCREEN_HEIGHT
	def triggerFullscreen(self) :
		self.set_fullscreen(not self.fullscreen)

	# Stop or play the music
	def triggerMusic(self) :
		if self.media_player.playing :
			self.media_player.pause()
		else :
			self.media_player.play()

	def isPlayingMusic(self) :
		return self.media_player.playing


# Main function to launche the game
def main() :
	""" Main method """
	game = AoCE()
	arcade.run()
