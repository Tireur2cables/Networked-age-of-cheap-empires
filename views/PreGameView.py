# Imports
import arcade
from arcade.gui.widgets import UITextArea, UITexturePane
from views.CustomButtons import SelctCivilButton, NextViewButton, NumInput
from views.FakeGameView import FakeGameView

#Constants
BACKGROUND_PREGAME = "./Ressources/img/FondAgePaint4.png" #A changer, c'est moche

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
		self.retourButton()

	#Boutton retour
	def retourButton(self):
		buttonsize = self.window.width/6

		# Create a vertical BoxGroup to align buttons
		self.v_box = arcade.gui.UIBoxLayout()

		quit_button = NextViewButton(
			self.window, self.main_view,
			text="Return",
			width=buttonsize
		)
		self.v_box.add(quit_button)

		# Create a widget to hold the v_box widget, that will center the buttons
		self.manager.add(
			arcade.gui.UIAnchorWidget(
				anchor_x = "left",
				align_x = buttonsize*(0.1),
				anchor_y = "top",
				align_y= -buttonsize*(0.1),
				child = self.v_box
			)
		)


	def setupButtons(self):
		# def button size
		buttonsize = self.window.width / 6

		# Create a vertical BoxGroup to align buttons
		self.v_box = arcade.gui.UIBoxLayout()

		# Create the buttons of incrementation
		you_civil_button = SelctCivilButton(
			self.window,
			text="Vous : Civilisation",
			size=buttonsize,
			name="Vous"
		)
		self.v_box.add(you_civil_button.with_space_around(bottom=20))

		name = ["Hugot", "Nico", "GuiLeDav", "Maxence", "Thomas", "Kenzo", "Nicolas"]

		for i in range(self.nbAdv) :
			adv1_civil_button = SelctCivilButton(
				self.window, text=name[i] + " : Civilisation",
				size=buttonsize,name=name[i]
			)
			self.v_box.add(adv1_civil_button.with_space_around(bottom=20))

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

	#New class ad by GuiLeDav 22/11/2021, affiche la gestion du nombre de ressources
	def ressourcesInput(self) :
		# def button size
		buttonsize = self.window.width / 6

		#Couleur de fond pour les espaces ressources modifiables
		bg_text = arcade.load_texture("Ressources/img/grey_fond.jpg")

		#Creation du text "Ressource :"
		ressource_text = UITextArea(
			x=self.window.width - buttonsize*(3/2),
			y=self.window.height - buttonsize*(0.75),
			width=buttonsize/2,
			height=buttonsize/10,
			text="Ressources :",
			text_color=(0, 0, 0, 255)
		)

		name_ressources = ["Or : ", "Bois : ", "Nourriture : ", "Pierre : "]

		#COMPLETEMENT DINGUE : le nom de ressource sous format "" est écrasé mais après qu'on est
		#deja implemente la valeur "" a notre fonction, diront nous.
		for i in range(len(name_ressources)) :
			name_ressources[i]= UITextArea(
				x=self.window.width - buttonsize*(3/2),
				y=self.window.height - buttonsize*(1.25+i*0.25),
				width=buttonsize/3,
				height=buttonsize/11,
				text=name_ressources[i],
				text_color=(0, 0, 0, 255)
			)

			self.manager.add(
				UITexturePane(
					name_ressources[i].with_space_around(right=20),
					tex=bg_text,
					padding=(10, 10, 10, 10)
				)
			)

		#Creation des espaces ressources modifiables
		name_input_ressources = ["Or_input", "Bois_input", "Nourriture_input", "Pierre_input"]

		for i in range(len(name_input_ressources)) :
			name_input_ressources[i] = arcade.gui.UITexturePane(
				NumInput(
					x=self.window.width - buttonsize/(1.4),
					y=self.window.height - buttonsize*(1.25+i*0.25),
					text="200", width=buttonsize/(2.5), height=buttonsize/10,
					text_color=(1, 1, 1, 255)
				),
				tex=bg_text
			)
			#Affichage des espaces ressources modifiables
			self.manager.add(name_input_ressources[i])

		#Affichage de "Ressource :"
		self.manager.add(
			UITexturePane(
				ressource_text.with_space_around(right=20),
				tex=bg_text,
				padding=(10, 10, 10, 10)
			)
		)

	#Button to start the game
	def launch_game(self):
		# def button size
		buttonsize = self.window.width / 6

		# Create a vertical BoxGroup to align buttons
		self.v_box = arcade.gui.UIBoxLayout()

		# Create the button
		num_enem_button = NextViewButton(
			self.window,
			PreGameView(
				self.main_view,
				self.nbAdv+1
			),
			text="Nombre d'adversaire : " + str(self.nbAdv),
			width=buttonsize*(3/2)
		)
		self.v_box.add(num_enem_button.with_space_around(bottom=20))

		launch_button = NextViewButton(
			self.window,
			FakeGameView(),
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
				align_y = -buttonsize,
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
