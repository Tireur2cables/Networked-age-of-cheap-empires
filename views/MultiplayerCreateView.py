# Imports
import arcade
from player import Player
from views.CustomButtons import NumInput, SelctDifButton, NextViewButton, LaunchOnlineGameButton, OnlinePlayerButton
from views.PreGameView import PreGameView
from network.pytoc import *

button_texture = "Ressources/img/button_background.png"

class MultiplayerCreateView(PreGameView):

	def __init__(self, main_view) :
		super().__init__(main_view)
		self.count = 0

	def setup(self) :
		# tell the game to activate multiplayer mode
		self.window.activate_multiplayer_host()
		# add an UIManager to handle the UI.
		self.manager = arcade.gui.UIManager()

	def pseudoBox(self):
		buttonsize = self.window.width / 10 # arbitrary

		bg_pseudo = arcade.load_texture(button_texture)
		pseudo_area = arcade.gui.UITextArea(
			x = self.window.width / 6,
			y = self.window.height / 1.1,
			width = buttonsize,
			height = buttonsize / 3,
			text = "Votre pseudo : " + self.window.pseudo
			)

		self.manager.add(
			arcade.gui.UITexturePane(
			pseudo_area.with_space_around(left = buttonsize / 3, right = buttonsize / 3),
			tex = bg_pseudo,
			padding = (10,10,10,10)
			)
		)

	def setupButtons(self) :
		# def button size
		buttonsize = self.window.width / 6 # arbitrary

		# Create a vertical BoxGroup to align buttons
		self.players_box = arcade.gui.UIBoxLayout()

		you_civil_button = OnlinePlayerButton(text=self.window.pseudo, width=buttonsize * 2, height=buttonsize / 4)
		self.players_box.add(you_civil_button.with_space_around(bottom=20))

		self.pseudoBox()

		# Create a widget to hold the v_box widget, that will center the buttons
		self.manager.add(
			arcade.gui.UIAnchorWidget(
				anchor_x = "left",
				align_x = buttonsize / 2,
				anchor_y = "top",
				align_y= -buttonsize * (3 / 5),
				child = self.players_box
			)
		)

	def add_player(self, pseudo) :
		buttonsize = self.window.width / 6 # arbitrary
		new_civil_button = OnlinePlayerButton(text=pseudo, width=buttonsize * 2, height=buttonsize / 4)
		self.players_box.add(new_civil_button.with_space_around(bottom=20))

	def remove_player(self, pseudo) :
		for button in self.players_box.children :
			if button.child.text == pseudo + " : Joueur en ligne" :
				self.players_box.remove(button)
				break

	#Button to start the game
	def launch_game(self) :
		# def button size
		buttonsize = self.window.width / 6 # arbitrary

		# Create a vertical BoxGroup to align buttons
		self.launch_box = arcade.gui.UIBoxLayout()

		launch_button = LaunchOnlineGameButton(
			self.window,
			self.main_view.game_view,
			self,
			text="Lancer la partie",
			width=buttonsize * (3 / 2)
		)
		self.launch_box.add(launch_button.with_space_around(bottom=20))

		# Create a widget to hold the v_box widget, that will center the buttonsS
		self.manager.add(
			arcade.gui.UIAnchorWidget(
				anchor_x = "right",
				align_x = -buttonsize * (0.2),
				anchor_y = "center_y",
				align_y= -buttonsize,
				child = self.launch_box
			)
		)

	def on_update(self, delta_time) :
		self.count += 1
		if (self.count == 30) : # changer si trop rapide ou trop long
			s = receive_string(self.window.lecture_fd)
			if s :
				print(s)
				flag, pseudo = s.split(" ")
				match flag :
					case "NEW" : self.add_player(pseudo)
					case "DECO" : self.remove_player(pseudo)
					case _: print(s)
			self.count = 0
