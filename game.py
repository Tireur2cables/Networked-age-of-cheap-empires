# --- Imports ---
# -- libs --
import random
# -- arcade --
import arcade
from player import AI, Player
# -- others --
from views.MainView import MainView
# -- mvc --
from Model import Model
from Controller import Controller
from View import View
# -- network --
from network.pytoc import *

from CONSTANTS import Resource as res

# --- Constants ---
DEFAULT_SCREEN_WIDTH = 800
DEFAULT_SCREEN_HEIGHT = 600
SCREEN_TITLE = "Age Of Cheap Empire"

MUSIC = "./Ressources/music/NEW_AGE.mp3"
USERNAME_FILE = "./usernames.list"

# --- Launch setup ---
from LAUNCH_SETUP import LAUNCH_FULLSCREEN, LAUNCH_MUSIC

#########################################################################
#							MAIN CLASS									#
#########################################################################

class AoCE(arcade.Window):

	ecriture_fd = None
	lecture_fd = None

	def __init__(self):
		""" Initializer """
		# Call the initializer of arcade.Window
		super().__init__(DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT, SCREEN_TITLE, resizable=False, fullscreen=LAUNCH_FULLSCREEN, vsync=True)
		#arcade.set_background_color(arcade.csscolor.WHITE)
		self.set_update_rate(1/60)#set maximum fps

		# Show the mouse cursor
		self.set_mouse_visible(True)
		arcade.enable_timings(20)

		# Lance la musique
		self.my_music = arcade.load_sound(MUSIC, streaming=True)
		self.media_player = self.my_music.play(loop=True)
		if not LAUNCH_MUSIC:
			self.media_player.pause()

		self.GameView = GameView()
		# # Variables for communications between model, view and controller.
		# self.toDraw = []
		self.tactilmod = False
		self.pseudo = self.getPseudo();
		self.multiplayer = False
		self.ecriture_fd = AoCE.ecriture_fd
		self.lecture_fd = AoCE.lecture_fd

	def getPseudo(self) :
		pseudo = "Default pseudo"
		with open(USERNAME_FILE) as file:
			tab = file.read().splitlines();
			pseudo = random.choice(tab)
			pseudo += str(random.choice(range(0,100)))
		return pseudo

	def activate_multiplayer_host(self) :
		self.multiplayer = True
		mess = "INIT " + self.pseudo
		send(mess, AoCE.ecriture_fd)

	def activate_multiplayer(self) :
		self.multiplayer = True
		mess = "JOIN " + self.pseudo
		send(mess, AoCE.ecriture_fd)

	def desactivate_multiplayer(self) :
		self.multiplayer = False
		send("CANCEL", AoCE.ecriture_fd)

	def on_show(self):
		# Affiche le main menu
		start_view = MainView(self.GameView)
		self.GameView.setMenuView(start_view)
		start_view.setup() # useless : mainview.setup is empty
		self.show_view(start_view)

	# Stop all process and exit arcade
	def exit(self):
		self.media_player.delete()
		arcade.exit()
		send("STOP", AoCE.ecriture_fd)

	def triggerTactil(self) :
		self.tactilmod = not self.tactilmod
		self.GameView.tactilmod = self.tactilmod

	# Set fullscreen or defaults : SCREEN_WIDTH x SCREEN_HEIGHT
	def triggerFullscreen(self) :
		curr = self.current_view
		curr.on_hide_view()
		self.set_fullscreen(not self.fullscreen)
		self.show_view(curr)

	# Stop or play the music
	def triggerMusic(self):
		if self.media_player.playing:
			self.media_player.pause()
		else:
			self.media_player.play()

	# Active or not the vsync
	def triggerVsync(self) :
		self.set_vsync(not self.vsync)

	def isPlayingMusic(self) :
		return self.media_player.playing


#########################################################################
#							GAME VIEW									#
#########################################################################
# In game view
class GameView(arcade.View):

	def __init__(self):
		super().__init__()
		self.menu_view = None
		# Créer l'architecture MVC
		self.game_model = Model(self)
		self.game_view = View(self)  # Je ne sais pas comment modifier autrement la valeur de "set_mouse_visible"
		self.game_controller = Controller(self)
		self.players = dict()
		self.tactilmod = False # initialised by aoce

	def setMenuView(self, menu_view):
		self.menu_view = menu_view

	def create_players(self, players, resources):
		i = 1
		human_in_game = False
		ia_in_game = False
		for name in resources :
			n = ""
			if name == res.FOOD :
				n = "FOOD"
			elif name == res.WOOD :
				n = "WOOD"
			elif name == res.GOLD :
				n = "GOLD"
			else :
				n = "STONE"

			txt = "RES " + n + " " + str(resources[name])
			send(txt, AoCE.ecriture_fd)
		for player, difficulty in players.items():
			if "Joueur Humain" in difficulty[0] or "Joueur en ligne" in difficulty[0] :
				self.players[player] = Player(self, player, resources, difficulty[1])
				human_in_game = True
				txt = "CR " + player + " " + str(difficulty[1])
				send(txt, AoCE.ecriture_fd)
			else:
				self.players[f"ai_{i}"] = AI(self, f"ai_{i}", difficulty, resources)
				i += 1
				ia_in_game = True
		return human_in_game, ia_in_game


	def setup(self, ressources, players, map_seed):
		""" Set up the game and initialize the variables. (Re-called when we want to restart the game without exiting it)."""
		human_in_game, ia_in_game = self.create_players(players, ressources)
		# self.players = {"player": Player(self, "player", ressources), "ai_1": AI(self, "ai_1", ressources)}
		if human_in_game and ia_in_game:
			self.game_controller.setup(self.players, "JvsIA")
		elif ia_in_game:
			self.game_controller.setup(self.players, "IAvsIA")
		elif human_in_game and len(self.players) == 1:
			self.game_controller.setup(self.players, "J")
		else:
			self.game_controller.setup(self.players, "JvsJ")
			send(str(map_seed), AoCE.ecriture_fd)
		self.game_model.setup(ressources, self.players.keys(), map_seed)
		self.game_view.setup(self.tactilmod)

	def load_save(self, data):
		# in data : {'model': game.game_model, 'controller': game.game_controller, 'players': game.players}
		self.players = data['players']
		self.game_model = data['model']
		self.game_view.setup(self.tactilmod)
		self.game_controller = data['controller']


		for player in self.players.values():
			player.game = self
		self.game_model.game = self
		self.game_view.game = self
		self.game_controller.game = self

	def reset_game(self):
		for player in self.players.values():
			player.reset()
		self.players.clear()
		self.game_model.reset()
		self.game_view.reset()
		self.game_controller.reset()

	def on_update(self, *args):  # Redirecting on_update to the Controller
		self.game_controller.on_update(*args)

	def on_key_press(self, *args):
		self.game_view.on_key_press(*args)

	def on_mouse_press(self, *args):  # Redirecting inputs to the View
		self.game_view.on_mouse_press(*args)

	def on_mouse_motion(self, *args):
		self.game_view.on_mouse_motion(*args)

	def on_draw(self):
		self.game_view.on_draw()

	def on_show(self):
		self.game_view.on_show()

	def on_hide_view(self):
		self.game_view.on_hide_view()



# Main function to launch the game
def main(ecriture_fd = None, lecture_fd = None):
	""" Main method """
	AoCE.ecriture_fd = int(ecriture_fd)
	AoCE.lecture_fd = int(lecture_fd)
	game = AoCE()
	arcade.run()
