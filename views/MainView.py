# Imports
import arcade
from arcade.arcade_types import Color
from arcade.gui.widgets import UIFlatButton
from views.CustomButtons import QuitButton, NextViewButton, CheckboxButton, SelctCivilButton
import random

#############################################################
#						Main View							#
#############################################################

# Constants
BACKGROUND = "./Ressources/img/background.png"

# View d'accueil : première à etre affichée à l'écran
class MainView(arcade.View) :

	def __init__(self, game_view) :
		super().__init__()
		self.game_view = game_view

	def setup(self) :
		pass

	def on_show(self):
		""" This is run once when we switch to this view """

		# ajoute l'image de background
		self.texture = arcade.load_texture(BACKGROUND)

		# add an UIManager to handle the UI.
		self.manager = arcade.gui.UIManager()
		self.manager.enable()

		self.setupButtons()

	def setupButtons(self):
		# def button size
		buttonsize = self.window.width / 6

		# Create a vertical BoxGroup to align buttons
		self.v_box = arcade.gui.UIBoxLayout()

		# Create the buttons

		start_button = NextViewButton(self.window, PreGameView(), text="Start Game VS IA", width=buttonsize)
		self.v_box.add(start_button.with_space_around(bottom=20))

		ia_match_button = NextViewButton(self.window,IAPreGameView(), text="IA VS IA Game",width=buttonsize)
		self.v_box.add(ia_match_button.with_space_around(bottom=20))

		map_button = NextViewButton(self.window, self.game_view, text="Show Map", width=buttonsize)
		self.v_box.add(map_button.with_space_around(bottom=20))

		settings_button = NextViewButton(self.window, SettingsView(self), text="Settings", width=buttonsize)
		self.v_box.add(settings_button.with_space_around(bottom=20))

		quit_button = QuitButton(self.window, text="Quit", width=buttonsize)
		self.v_box.add(quit_button)

		# Create a widget to hold the v_box widget, that will center the buttons
		self.manager.add(
			arcade.gui.UIAnchorWidget(
				anchor_x = "left",
				align_x = buttonsize,
				anchor_y = "center_y",
				align_y= -buttonsize/6,
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

#############################################################
#						Settings View						#
#############################################################

# Constants
SETTINGS_BACKGROUND = "./Ressources/img/LastImageSettings.jpg"

# View des paramètres accessible via ecran d'accueil
class SettingsView(arcade.View) :
	""" Settings view """

	def __init__(self, main_view) :
		super().__init__()
		self.main_view = main_view

	def on_show(self):
		""" This is run once when we switch to this view """

		# ajoute l'image de background
		self.texture = arcade.load_texture(SETTINGS_BACKGROUND)

		# a UIManager to handle the UI.
		self.manager = arcade.gui.UIManager()
		self.manager.enable()

		self.setupButtons()

	def setup(self) :
		pass

	def setupButtons(self) :
		# def sizes
		buttonsize = self.window.width / 6
		checkboxsize = buttonsize / 2

		# Create a vertical BoxGroup to align buttons
		self.v_box = arcade.gui.UIBoxLayout()

		# Create checkboxes
		music_button = CheckboxButton(self.window, text="Musique", size=checkboxsize, ticked=self.window.isPlayingMusic(), music=True)
		self.v_box.add(music_button.with_space_around(bottom=20))

		fullscreen_button = CheckboxButton(self.window, text="Plein écran", size=checkboxsize, ticked=self.window.fullscreen, fullscreen=True)
		self.v_box.add(fullscreen_button.with_space_around(bottom=20))

		# Create the return menu
		retour_button = NextViewButton(self.window, self.main_view, text="Retour", width=buttonsize)
		self.v_box.add(retour_button.with_space_around(bottom=20))

		# Create a widget to hold the v_box widget, that will center the buttons
		self.manager.add(
			arcade.gui.UIAnchorWidget(
				anchor_x = "center_x",
				anchor_y = "center_y",
				child = self.v_box
			)
		)

	def on_draw(self):
		""" Draw this view """
		arcade.start_render()

		self.texture.draw_sized(self.window.width / 2, self.window.height / 2, self.window.width, self.window.height)
		arcade.draw_text("Settings Screen", self.window.width / 2, self.window.height * 5 / 6, arcade.color.WARM_BLACK, font_size=50, anchor_x="center")

		self.manager.draw()


	def on_hide_view(self) :
		self.manager.disable()


#############################################################
#					PreGame Menu							#
#############################################################

#Constants
BACKGROUND_PREGAME = "./Ressources/img/ImageSettings.png" #A changer, c'est moche

class PreGameView(arcade.View):
	def setup(self) :
		pass

	def on_show(self):
		""" This is run once when we switch to this view """

		# ajoute l'image de background
		self.texture = arcade.load_texture(BACKGROUND_PREGAME)

		# add an UIManager to handle the UI.
		self.manager = arcade.gui.UIManager()
		self.manager.enable()

		self.setupButtons()
		self.NumEnemButton()
		self.launch_game()

	def setupButtons(self):
		# def button size
		buttonsize = self.window.width / 6

		# Create a vertical BoxGroup to align buttons
		self.v_box = arcade.gui.UIBoxLayout()

		# Create the buttons of incrementation
		you_civil_button = SelctCivilButton(self.window,text="Vous : Civilisation", size=buttonsize,name="Vous")
		self.v_box.add(you_civil_button.with_space_around(bottom=20))
		
		quit_button = NextViewButton(self.window,MainView(), text="Return", width=buttonsize)
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
	def NumEnemButton(self):

		# def button size
		buttonsize = self.window.width / 6

		# Create a vertical BoxGroup to align buttons
		self.v_box = arcade.gui.UIBoxLayout()

		# Create the button
		num_enem_button = NextViewButton(self.window, PreGameView2(), text="Nombre d'adversaire : 0", width=buttonsize)
		self.v_box.add(num_enem_button.with_space_around(bottom=20))

		# Create a widget to hold the v_box widget, that will center the buttons
		self.manager.add(
			arcade.gui.UIAnchorWidget(
				anchor_x = "left",
				align_x = buttonsize,
				anchor_y = "center_y",
				align_y= -buttonsize,
				child = self.v_box
			)
		)

	#Button to start the game
	def launch_game(self):
		# def button size
		buttonsize = self.window.width / 6

		# Create a vertical BoxGroup to align buttons
		self.v_box = arcade.gui.UIBoxLayout()

		# Create the button
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



####################################################### Second Window #######################################################
class PreGameView2(arcade.View):
	def setup(self) :
		pass

	def on_show(self):
		""" This is run once when we switch to this view """

		# ajoute l'image de background
		self.texture = arcade.load_texture(BACKGROUND_PREGAME)

		# add an UIManager to handle the UI.
		self.manager = arcade.gui.UIManager()
		self.manager.enable()
		self.setupButtons()
		self.NumEnemButton()
		self.launch_game()
		      
	def setupButtons(self):
		# def button size
		buttonsize = self.window.width / 6

		# Create a vertical BoxGroup to align buttons
		self.v_box = arcade.gui.UIBoxLayout()

		# Create the buttons of incrementation
		you_civil_button = SelctCivilButton(self.window,text="Vous : Civilisation", size=buttonsize,name="Vous")
		self.v_box.add(you_civil_button.with_space_around(bottom=20))

		adv1_civil_button = SelctCivilButton(self.window,text="Hugo : Civilisation", size=buttonsize,name="Hugo")
		self.v_box.add(adv1_civil_button.with_space_around(bottom=20))

		quit_button = NextViewButton(self.window,MainView(), text="Return", width=buttonsize)
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
	def NumEnemButton(self):

		# def button size
		buttonsize = self.window.width / 6

		# Create a vertical BoxGroup to align buttons
		self.v_box = arcade.gui.UIBoxLayout()

		# Create the button
		num_enem_button = NextViewButton(self.window, PreGameView3(), text="Nombre d'adversaire : 1", width=buttonsize)
		self.v_box.add(num_enem_button.with_space_around(bottom=20))

		# Create a widget to hold the v_box widget, that will center the buttons
		self.manager.add(
			arcade.gui.UIAnchorWidget(
				anchor_x = "left",
				align_x = buttonsize,
				anchor_y = "center_y",
				align_y= -buttonsize,
				child = self.v_box
			)
		)

	#Button to start the game
	def launch_game(self):
		# def button size
		buttonsize = self.window.width / 6

		# Create a vertical BoxGroup to align buttons
		self.v_box = arcade.gui.UIBoxLayout()

		# Create the button
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


####################################################### Third Window #######################################################
class PreGameView3(arcade.View):
	def setup(self) :
		pass

	def on_show(self):
		""" This is run once when we switch to this view """

		# ajoute l'image de background
		self.texture = arcade.load_texture(BACKGROUND_PREGAME)

		# add an UIManager to handle the UI.
		self.manager = arcade.gui.UIManager()
		self.manager.enable()
		self.setupButtons()
		self.NumEnemButton()
		self.launch_game()
		      
	def setupButtons(self):
		# def button size
		buttonsize = self.window.width / 6

		# Create a vertical BoxGroup to align buttons
		self.v_box = arcade.gui.UIBoxLayout()

		# Create the buttons of incrementation
		you_civil_button = SelctCivilButton(self.window,text="Vous : Civilisation", size=buttonsize,name="Vous")
		self.v_box.add(you_civil_button.with_space_around(bottom=20))

		adv1_civil_button = SelctCivilButton(self.window,text="Hugo : Civilisation", size=buttonsize,name="Hugo")
		self.v_box.add(adv1_civil_button.with_space_around(bottom=20))

		adv2_civil_button = SelctCivilButton(self.window,text="Thomas : Civilisation", size=buttonsize,name="Thomas")
		self.v_box.add(adv2_civil_button.with_space_around(bottom=20))

		quit_button = NextViewButton(self.window,MainView(), text="Return", width=buttonsize)
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
	def NumEnemButton(self):

		# def button size
		buttonsize = self.window.width / 6

		# Create a vertical BoxGroup to align buttons
		self.v_box = arcade.gui.UIBoxLayout()

		# Create the button
		num_enem_button = NextViewButton(self.window, PreGameView4(), text="Nombre d'adversaire : 2", width=buttonsize)
		self.v_box.add(num_enem_button.with_space_around(bottom=20))

		# Create a widget to hold the v_box widget, that will center the buttons
		self.manager.add(
			arcade.gui.UIAnchorWidget(
				anchor_x = "left",
				align_x = buttonsize,
				anchor_y = "center_y",
				align_y= -buttonsize,
				child = self.v_box
			)
		)

	#Button to start the game
	def launch_game(self):
		# def button size
		buttonsize = self.window.width / 6

		# Create a vertical BoxGroup to align buttons
		self.v_box = arcade.gui.UIBoxLayout()

		# Create the button
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

####################################################### Fourth Window #######################################################
class PreGameView4(arcade.View):
	def setup(self) :
		pass
	def on_show(self):
		""" This is run once when we switch to this view """

		# ajoute l'image de background
		self.texture = arcade.load_texture(BACKGROUND_PREGAME)

		# add an UIManager to handle the UI.
		self.manager = arcade.gui.UIManager()
		self.manager.enable()
		self.setupButtons()
		self.NumEnemButton()
		self.launch_game()
		      
	def setupButtons(self):
		# def button size
		buttonsize = self.window.width / 6

		# Create a vertical BoxGroup to align buttons
		self.v_box = arcade.gui.UIBoxLayout()

		# Create the buttons of incrementation
		you_civil_button = SelctCivilButton(self.window,text="Vous : Civilisation", size=buttonsize,name="Vous")
		self.v_box.add(you_civil_button.with_space_around(bottom=20))

		adv1_civil_button = SelctCivilButton(self.window,text="Hugo : Civilisation", size=buttonsize,name="Hugo")
		self.v_box.add(adv1_civil_button.with_space_around(bottom=20))

		adv2_civil_button = SelctCivilButton(self.window,text="Thomas : Civilisation", size=buttonsize,name="Thomas")
		self.v_box.add(adv2_civil_button.with_space_around(bottom=20))

		adv3_civil_button = SelctCivilButton(self.window,text="Nicolas : Civilisation", size=buttonsize,name="Nicolas")
		self.v_box.add(adv3_civil_button.with_space_around(bottom=20))

		quit_button = NextViewButton(self.window,MainView(), text="Return", width=buttonsize)
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
	def NumEnemButton(self):

		# def button size
		buttonsize = self.window.width / 6

		# Create a vertical BoxGroup to align buttons
		self.v_box = arcade.gui.UIBoxLayout()

		# Create the button
		num_enem_button = NextViewButton(self.window, PreGameView5(), text="Nombre d'adversaire : 3", width=buttonsize)
		self.v_box.add(num_enem_button.with_space_around(bottom=20))

		# Create a widget to hold the v_box widget, that will center the buttons
		self.manager.add(
			arcade.gui.UIAnchorWidget(
				anchor_x = "left",
				align_x = buttonsize,
				anchor_y = "center_y",
				align_y= -buttonsize,
				child = self.v_box
			)
		)

	#Button to start the game
	def launch_game(self):
		# def button size
		buttonsize = self.window.width / 6

		# Create a vertical BoxGroup to align buttons
		self.v_box = arcade.gui.UIBoxLayout()

		# Create the button
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

####################################################### Fifth Window #######################################################
class PreGameView5(arcade.View):
	def setup(self) :
		pass
	def on_show(self):
		""" This is run once when we switch to this view """

		# ajoute l'image de background
		self.texture = arcade.load_texture(BACKGROUND_PREGAME)

		# add an UIManager to handle the UI.
		self.manager = arcade.gui.UIManager()
		self.manager.enable()
		self.setupButtons()
		self.NumEnemButton()
		self.launch_game()
		      
	def setupButtons(self):
		# def button size
		buttonsize = self.window.width / 6

		# Create a vertical BoxGroup to align buttons
		self.v_box = arcade.gui.UIBoxLayout()

		# Create the buttons of incrementation
		you_civil_button = SelctCivilButton(self.window,text="Vous : Civilisation", size=buttonsize,name="Vous")
		self.v_box.add(you_civil_button.with_space_around(bottom=20))

		adv1_civil_button = SelctCivilButton(self.window,text="Hugo : Civilisation", size=buttonsize,name="Hugo")
		self.v_box.add(adv1_civil_button.with_space_around(bottom=20))

		adv2_civil_button = SelctCivilButton(self.window,text="Thomas : Civilisation", size=buttonsize,name="Thomas")
		self.v_box.add(adv2_civil_button.with_space_around(bottom=20))

		adv3_civil_button = SelctCivilButton(self.window,text="Nicolas : Civilisation", size=buttonsize,name="Nicolas")
		self.v_box.add(adv3_civil_button.with_space_around(bottom=20))

		adv4_civil_button = SelctCivilButton(self.window,text="Kenzo : Civilisation", size=buttonsize,name="Kenzo")
		self.v_box.add(adv4_civil_button.with_space_around(bottom=20))

		quit_button = NextViewButton(self.window,MainView(), text="Return", width=buttonsize)
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
	def NumEnemButton(self):

		# def button size
		buttonsize = self.window.width / 6

		# Create a vertical BoxGroup to align buttons
		self.v_box = arcade.gui.UIBoxLayout()

		# Create the button
		num_enem_button = NextViewButton(self.window, PreGameView(), text="Nombre d'adversaire : 4", width=buttonsize)
		self.v_box.add(num_enem_button.with_space_around(bottom=20))

		# Create a widget to hold the v_box widget, that will center the buttons
		self.manager.add(
			arcade.gui.UIAnchorWidget(
				anchor_x = "left",
				align_x = buttonsize,
				anchor_y = "center_y",
				align_y= -buttonsize,
				child = self.v_box
			)
		)
	
	#Button to start the game
	def launch_game(self):
		# def button size
		buttonsize = self.window.width / 6

		# Create a vertical BoxGroup to align buttons
		self.v_box = arcade.gui.UIBoxLayout()

		# Create the button
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

#############################################################
#					IA VS IA View							#
#############################################################		

#Constants
BACKGROUND_IAPREGAME = "./Ressources/img/ImageSettings.png" #A changer, c'est moche

class IAPreGameView(arcade.View):
	def setup(self) :
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

	def setupButtons(self):
		# def button size
		buttonsize = self.window.width / 6

		# Create a vertical BoxGroup to align buttons
		self.v_box = arcade.gui.UIBoxLayout()

		# Create the buttons of incrementation
		ia1_civil_button = SelctCivilButton(self.window,text="IA1: Civilisation", size=buttonsize,name="IA1")
		self.v_box.add(ia1_civil_button.with_space_around(bottom=20))

		ia2_civil_button = SelctCivilButton(self.window,text="IA2: Civilisation", size=buttonsize,name="IA2")
		self.v_box.add(ia2_civil_button.with_space_around(bottom=20))
		
		quit_button = NextViewButton(self.window,MainView(), text="Return", width=buttonsize)
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
	def NumEnemButton(self):

		# def button size
		buttonsize = self.window.width / 6

		# Create a vertical BoxGroup to align buttons
		self.v_box = arcade.gui.UIBoxLayout()

		# Create the button
		num_enem_button = NextViewButton(self.window, PreGameView2(), text="Nombre d'adversaire : 0", width=buttonsize)
		self.v_box.add(num_enem_button.with_space_around(bottom=20))

		# Create a widget to hold the v_box widget, that will center the buttons
		self.manager.add(
			arcade.gui.UIAnchorWidget(
				anchor_x = "left",
				align_x = buttonsize,
				anchor_y = "center_y",
				align_y= -buttonsize,
				child = self.v_box
			)
		)
	
	#Button to start the game
	def launch_game(self):
		# def button size
		buttonsize = self.window.width / 6

		# Create a vertical BoxGroup to align buttons
		self.v_box = arcade.gui.UIBoxLayout()

		# Create the button
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

#############################################################
#					Fake Game								#
#############################################################

# --- Constants ---
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_COIN = .25
COIN_COUNT = 50
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Age Of Cheap Empire"

class FakeGameView(arcade.View):
	""" Our custom Window Class"""

	def __init__(self):
		""" Initializer """
		# Call the parent class initializer
		super().__init__()

		# Variables that will hold sprite lists
		self.player_list = None
		self.coin_list = None

		# Set up the player info
		self.player_sprite = None
		self.score = 0

	def setup(self) :
		pass

	def on_show(self):
		""" Set up the game and initialize the variables. """
		arcade.set_background_color(arcade.color.AMAZON)

		# Don't show the mouse cursor
		self.window.set_mouse_visible(False)

		# Sprite lists
		self.player_list = arcade.SpriteList()
		self.coin_list = arcade.SpriteList()

		# Score
		self.score = 0

		# Set up the player
		# Character image from kenney.nl
		self.player_sprite = arcade.Sprite(":resources:images/animated_characters/female_person/femalePerson_idle.png", SPRITE_SCALING_PLAYER)
		self.player_sprite.center_x = 50
		self.player_sprite.center_y = 50
		self.player_list.append(self.player_sprite)

		# Create the coins
		for i in range(COIN_COUNT):

			# Create the coin instance
			# Coin image from kenney.nl
			coin = arcade.Sprite(":resources:images/items/coinGold.png", SPRITE_SCALING_COIN)

			# Position the coin
			coin.center_x = random.randrange(SCREEN_WIDTH)
			coin.center_y = random.randrange(SCREEN_HEIGHT)

			# Add the coin to the lists
			self.coin_list.append(coin)

	def on_draw(self):
		""" Draw everything """
		arcade.start_render()
		self.coin_list.draw()
		self.player_list.draw()

		# Put the text on the screen.
		output = f"Score: {self.score}"
		arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

	def on_mouse_motion(self, x, y, dx, dy):
		""" Handle Mouse Motion """

		# Move the center of the player sprite to match the mouse x, y
		self.player_sprite.center_x = x
		self.player_sprite.center_y = y

	def on_update(self, delta_time):
		""" Movement and game logic """

		# Call update on all sprites (The sprites don't do much in this
		# example though.)
		self.coin_list.update()

		# Generate a list of all sprites that collided with the player.
		coins_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)

		# Loop through each colliding sprite, remove it, and add to the score.
		for coin in coins_hit_list:
			coin.remove_from_sprite_lists()
			self.score += 1
