# Imports
import arcade
from player import Player
from views.CustomButtons import NumInput, SelctDifButton, NextViewButton, LaunchGameButton, OnlinePlayerButton
from views.PreGameView import PreGameView

class MultiplayerGameView(PreGameView):

	def __init__(self, main_view) :
		super().__init__(main_view)

	def setup(self) :
		# add an UIManager to handle the UI.
		self.manager = arcade.gui.UIManager()

	def pseudoBox(self):
		buttonsize = self.window.width / 10 # arbitrary

		self.manager.add(
			arcade.gui.UITextArea(
				x=self.window.width / 10,
				y=self.window.height * 0.9,
				width = buttonsize,
				height = buttonsize,
				text=self.window.pseudo)
		)

	def setupButtons(self) :
		# def button size
		buttonsize = self.window.width / 6 # arbitrary

		# Create a vertical BoxGroup to align buttons
		self.players_box = arcade.gui.UIBoxLayout()

		you_civil_button = OnlinePlayerButton(text=self.window.pseudo, width=buttonsize * 2, height=buttonsize / 4)
		self.players_box.add(you_civil_button.with_space_around(bottom=20))

		"""
		name = ["IA1", "IA2", "IA3 ", "IA4", "IA5", "IA6", "IA7", "IA8"]

		for i in range(self.nbAdv) :
			ia_button = SelctDifButton(text=name[i], size=buttonsize, name=name[i])
			self.ia_box.add(ia_button.with_space_around(bottom=20))
		"""

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

	#Button to start the game
	def launch_game(self) :
		# def button size
		buttonsize = self.window.width / 6 # arbitrary

		# Create a vertical BoxGroup to align buttons
		self.launch_box = arcade.gui.UIBoxLayout()
		"""
		# Create the button
		num_enem_button = NextViewButton(
			self.window,
			MultiplayerGameView(self.main_view, self.nbAdv + 1),
			text="Nombre d'IA : " + str(self.nbAdv),
			width=buttonsize * (3 / 2)
		)

		self.launch_box.add(num_enem_button.with_space_around(bottom=20))
		"""
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
