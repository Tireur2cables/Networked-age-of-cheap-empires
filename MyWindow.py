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
		#self.media_player.push_handlers(on_eos=self.music_over)

		# Stop la musique
		#self.media_player.stop()

		# affiche la souris
		self.set_mouse_visible(True)

	# def music_over(self):
		# self.media_player.pop_handlers()
		# self.media_player = None
		# #self.sound_button_off()
		# self.cur_song_index += 1
		# if self.cur_song_index >= len(self.songs):
		# 	self.cur_song_index = 0
		# self.my_music = arcade.load_sound(MUSIC)
		# self.media_player = self.my_music.play()
		# self.media_player.push_handlers(on_eos=self.music_over)
