# Imports
import arcade
from views.CustomButtons import SelctCivilButton, NextViewButton
from views.FakeGameView import FakeGameView

#Constants
BACKGROUND_IAPREGAME = "./Ressources/img/ImageSettings.png" #A changer, c'est moche

class IAPreGameView(arcade.View):
	def __init__(self, main_view,nbAdv=0) :
		super().__init__()
		self.main_view = main_view
		self.nbAdv = nbAdv

	def setup(self) :
		if self.nbAdv == 7 :
			self.nbAdv = 0
		pass

	def on_show(self):
		""" This is run once when we switch to this view """

		# ajoute l'image de background
		self.texture = arcade.load_texture(BACKGROUND_IAPREGAME)

		# add an UIManager to handle the UI.
		self.manager = arcade.gui.UIManager()
		self.manager.enable()

		self.setupButtons()
		self.launch_game()
##
#	def setupButtons(self):
		# def button size
#		buttonsize = self.window.width / 6

		# Create a vertical BoxGroup to align buttons
#		self.v_box = arcade.gui.UIBoxLayout()

		# Create the buttons of incrementation
#		ia1_civil_button = SelctCivilButton(self.window,text="IA1: Civilisation", size=buttonsize,name="IA1")
#		self.v_box.add(ia1_civil_button.with_space_around(bottom=20))

#		ia2_civil_button = SelctCivilButton(self.window,text="IA2: Civilisation", size=buttonsize,name="IA2")
#		self.v_box.add(ia2_civil_button.with_space_around(bottom=20))

#		quit_button = NextViewButton(self.window, self.main_view, text="Return", width=buttonsize)
#		self.v_box.add(quit_button)

		# Create a widget to hold the v_box widget, that will center the buttons
#		self.manager.add(
#			arcade.gui.UIAnchorWidget(
#				anchor_x = "left",
#				align_x = buttonsize/2,
#				anchor_y = "top",
#				align_y= -buttonsize/3,
#				child = self.v_box
#			)
#		)
##
	def setupButtons(self):
		# def button size
		buttonsize = self.window.width / 6

		# Create a vertical BoxGroup to align buttons
		self.v_box = arcade.gui.UIBoxLayout()

		# Create the buttons of incrementation
		ia1_civil_button = SelctCivilButton(self.window, text="IA1 : Civilisation", size=buttonsize,name="IA1")
		self.v_box.add(ia1_civil_button.with_space_around(bottom=20))

		ia2_civil_button = SelctCivilButton(self.window, text="IA2 : Civilisation", size=buttonsize,name="IA2")
		self.v_box.add(ia2_civil_button.with_space_around(bottom=20))

		name = ["IA3 ", "IA4", "IA5", "IA6", "IA7", "IA8"]

		for i in range(self.nbAdv) :
			adv1_civil_button = SelctCivilButton(self.window, text=name[i] + " : Civilisation", size=buttonsize,name=name[i])
			self.v_box.add(adv1_civil_button.with_space_around(bottom=20))

		quit_button = NextViewButton(self.window, self.main_view, text="Return", width=buttonsize)
		self.v_box.add(quit_button)

		# Create a widget to hold the v_box widget, that will center the buttons
		self.manager.add(
			arcade.gui.UIAnchorWidget(
				anchor_x = "left",
				align_x = buttonsize/2,
				anchor_y = "top",
				align_y= -buttonsize/3,
				child = self.v_box
			)
		)

	#Button for numbers of ennemi, it will be at the bottom of the window and in every pregame view
#	def NumEnemButton(self):
#
#		# def button size
#		buttonsize = self.window.width / 6

		# Create a vertical BoxGroup to align buttons
#		self.v_box = arcade.gui.UIBoxLayout()

		# Create the button
#		num_enem_button = NextViewButton(self.window, PreGameView(self.main_view), text="Nombre d'adversaire : 0", width=buttonsize)
#		self.v_box.add(num_enem_button.with_space_around(bottom=20))

		# Create a widget to hold the v_box widget, that will center the buttons
#		self.manager.add(
#			arcade.gui.UIAnchorWidget(
#				anchor_x = "left",
#				align_x = buttonsize,
#				anchor_y = "center_y",
#				align_y= -buttonsize,
#				child = self.v_box
#			)
#		)

	#Button to start the game
	def launch_game(self):
		# def button size
		buttonsize = self.window.width / 6

		# Create a vertical BoxGroup to align buttons
		self.v_box = arcade.gui.UIBoxLayout()

		# Create the button
		num_enem_button = NextViewButton(self.window, IAPreGameView(self.main_view, self.nbAdv+1), text="Nombre d'IA : " + str(self.nbAdv), width=buttonsize*(3/2))
		self.v_box.add(num_enem_button.with_space_around(bottom=20))

		launch_button = NextViewButton(self.window, FakeGameView(), text="Lancer la partie", width=buttonsize*(3/2))
		self.v_box.add(launch_button.with_space_around(bottom=20))

		# Create a widget to hold the v_box widget, that will center the buttonsS
		self.manager.add(
			arcade.gui.UIAnchorWidget(
				anchor_x = "right",
				align_x = -buttonsize,
				anchor_y = "center_y",
				align_y= -buttonsize,
				child = self.v_box
			)
		)

	def on_draw(self):
		""" Draw this view """

		arcade.start_render()
		self.texture.draw_sized(self.window.width / 2, self.window.height / 2, self.window.width, self.window.height)
		self.manager.draw()


	def on_hide_view(self) :
		self.manager.disable()
