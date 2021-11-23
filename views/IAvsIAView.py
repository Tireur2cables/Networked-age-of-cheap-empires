# Imports
import arcade
from views.CustomButtons import NumInput, SelctCivilButton, NextViewButton
from views.FakeGameView import FakeGameView
from views.PreGameView import PreGameView

class IAPreGameView(PreGameView) :

	def __init__(self, main_view, nbAdv=2) :
		super().__init__(main_view, nbAdv)
		self.isPlayer = False

	def setup(self) :
		if self.nbAdv == 9 :
			self.nbAdv = 2

	def setupButtons(self) :
		# def button size
		buttonsize = self.window.width / 6

		# Create a vertical BoxGroup to align buttons
		self.v_box = arcade.gui.UIBoxLayout()

		name = ["IA1", "IA2", "IA3 ", "IA4", "IA5", "IA6", "IA7", "IA8"]

		for i in range(self.nbAdv) :
			adv_civil_button = SelctCivilButton(
				self.window,
				text=name[i] + " : Civilisation",
				size=buttonsize,
				name=name[i]
			)
			self.v_box.add(adv_civil_button.with_space_around(bottom=20))

		# Create a widget to hold the v_box widget, that will center the buttons
		self.manager.add(
			arcade.gui.UIAnchorWidget(
				anchor_x = "left",
				align_x = buttonsize/2,
				anchor_y = "top",
				align_y= -buttonsize*(3/5),
				child = self.v_box
			)
		)

	#Button to start the game
	def launch_game(self) :
		# def button size
		buttonsize = self.window.width / 6

		# Create a vertical BoxGroup to align buttons
		self.v_box = arcade.gui.UIBoxLayout()

		# Create the button
		num_enem_button = NextViewButton(
			self.window,
			IAPreGameView(
				self.main_view,
				self.nbAdv+1
			),
			text="Nombre d'IA : " + str(self.nbAdv),
			width=buttonsize*(3/2)
		)
		self.v_box.add(num_enem_button.with_space_around(bottom=20))

		launch_button = NextViewButton(
			self.window,
			FakeGameView(
				self.name_input_ressources,
				self.nbAdv,
				self.isPlayer
			),
			text="Lancer la partie",
			width=buttonsize*(3/2)
		)
		self.v_box.add(launch_button.with_space_around(bottom=20))

		# Create a widget to hold the v_box widget, that will center the buttonsS
		self.manager.add(
			arcade.gui.UIAnchorWidget(
				anchor_x = "right",
				align_x = -buttonsize*(0.2),
				anchor_y = "center_y",
				align_y= -buttonsize,
				child = self.v_box
			)
		)
