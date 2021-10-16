# Imports
import arcade

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Age Of Cheap Empire"
MUSIC = "music/logon_aoe_music3s.wav"

# Main window : will contains all the view
class MyWindow(arcade.Window):
	def __init__(self):
		super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=False, fullscreen=True)

		# Lance la musique
		self.my_music = arcade.load_sound(MUSIC, streaming=True)
		self.media_player = self.my_music.play(loop=True)

		# affiche la souris
		self.set_mouse_visible(True)

	# Stop all process and exit arcade
	def exit(self) :
		self.media_player.delete()
		arcade.exit()

	# Stop or play the music
	def triggerMusic(self) :
		if self.media_player.playing :
			self.media_player.pause()
		else :
			self.media_player.play()

	# Set fulllscreen or 800 x 600
	def triggerFullscreen(self) :
		self.set_fullscreen(not self.fullscreen)
