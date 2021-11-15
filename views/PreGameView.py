# Imports
import arcade
from views.CustomButtons import SelctCivilButton, NextViewButton, NumInput
from views.FakeGameView import FakeGameView

#Constants
BACKGROUND_PREGAME = "./Ressources/img/ImageSettings.png" #A changer, c'est moche

class PreGameView(arcade.View):
	def __init__(self, main_view, nbAdv=0) :
		super().__init__()
		self.main_view = main_view
		self.nbAdv = nbAdv

	def setup(self) :
		if self.nbAdv == 8 :
			self.nbAdv = 0
		pass

	def on_show(self):
		""" This is run once when we switch to this view """

		# ajoute l'image de background
		self.texture = arcade.load_texture(BACKGROUND_PREGAME)

		# add an UIManager to handle the UI.
		self.manager = arcade.gui.UIManager()
		self.manager.enable()

		self.setupButtons()
		self.ressourcesInput()
		self.launch_game()

	def setupButtons(self):
		# def button size
		buttonsize = self.window.width / 6

		# Create a vertical BoxGroup to align buttons
		self.v_box = arcade.gui.UIBoxLayout()

		# Create the buttons of incrementation
		you_civil_button = SelctCivilButton(self.window, text="Vous : Civilisation", size=buttonsize,name="Vous")
		self.v_box.add(you_civil_button.with_space_around(bottom=20))

		name = ["Hugot", "Nico", "GuiLeDav", "Maxence", "Thomas", "Kenzo", "Nicolas"]

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

	def ressourcesInput(self) :
		# def button size
		buttonsize = self.window.width / 6

		bg_text = arcade.load_texture("Ressources/img/grey_fond.jpg")


		or_input = arcade.gui.UITexturePane(
			NumInput(x=self.window.width - buttonsize, y=self.window.height - buttonsize, text="200", width=buttonsize, height=buttonsize/3, text_color=(1, 1, 1, 255)),
			tex=bg_text
		)

		self.manager.add(
			or_input
		)



	#Button to start the game
	def launch_game(self):
		# def button size
		buttonsize = self.window.width / 6

		# Create a vertical BoxGroup to align buttons
		self.v_box = arcade.gui.UIBoxLayout()

		# Create the button
		num_enem_button = NextViewButton(self.window, PreGameView(self.main_view, self.nbAdv+1), text="Nombre d'adversaire : " + str(self.nbAdv), width=buttonsize*(3/2))
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
