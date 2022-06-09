# Imports
import arcade
from player import Player
from views.CustomButtons import NumInput, SelctDifButton, NextViewButton, LaunchGameButton, OnlinePlayerButton
from views.PreGameView import PreGameView
from views.inputIP import InputIP

button_texture = "Ressources/img/button_background.png"

class MultiplayerJoinView(PreGameView):

	def __init__(self, main_view) :
		super().__init__(main_view)

	def setup(self) :
		# add an UIManager to handle the UI.
		self.manager = arcade.gui.UIManager()
		self.join_game = 0


	def ip_box(self):

		buttonsize = self.window.width / 5
		join_game = InputIP(self.window, self.window.width/3,
		 	self.window.height/1.65,
			text="Entrez une IP",
			font_name="calibri",
			font_size=40,
			width=buttonsize,
			height=buttonsize
			)
		self.manager.add(join_game)

		join_game.reset_text()
		return join_game

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
		self.input_box = arcade.gui.UIBoxLayout()

		you_civil_button = OnlinePlayerButton(text=self.window.pseudo, width=buttonsize * 2, height=buttonsize / 4)
		self.players_box.add(you_civil_button.with_space_around(bottom=20))

		self.pseudoBox()
		self.join_game = self.ip_box()

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
		self.manager.add(self.input_box)

	#Button to start the game
	def launch_game(self):
		# def button size
		buttonsize = self.window.width / 6 # arbitrary

		# Create a vertical BoxGroup to align buttons
		self.launch_box = arcade.gui.UIBoxLayout()
		launch_button = LaunchGameButton(
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
