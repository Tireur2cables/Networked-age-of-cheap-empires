# Imports
import arcade
from player import Player
from views.CustomButtons import NumInput, SelctDifButton, NextViewButton, LaunchGameButton, OnlinePlayerButton, InputIP
from network.pytoc import *

from CONSTANTS import Resource as Res
BACKGROUND_PREGAME = "./Ressources/img/FondAgePaint5.jpg"
button_texture = "Ressources/img/button_background.png"

class MultiplayerJoinView(arcade.View):

	def __init__(self, main_view, nbAdv=0) :
		super().__init__()
		self.main_view = main_view
		self.nbAdv = nbAdv
		self.count = 0

	def setup(self) :
		# add an UIManager to handle the UI.
		self.manager = arcade.gui.UIManager()
		if self.nbAdv == 4:
			self.nbAdv = 0
		self.join_game = 0
		self.count = 0
		self.resources = {}
		self.seed = 0
		self.players = {}

	def on_show(self):
		""" This is run once when we switch to this view """

		# ajoute l'image de background
		self.texture = arcade.load_texture(BACKGROUND_PREGAME)

		self.manager.enable()

		self.setupButtons()
		self.retourButton()

	# Boutton retour
	def retourButton(self):
		buttonsize = self.window.width / 10 # arbitrary

		# Create a vertical BoxGroup to align buttons
		self.retour_box = arcade.gui.UIBoxLayout()

		retour_button = NextViewButton(self.window, self.main_view, text="Retour", width=buttonsize)
		self.retour_box.add(retour_button)

		# Create a widget to hold the v_box widget, that will center the buttons
		self.manager.add(
			arcade.gui.UIAnchorWidget(
				anchor_x = "left",
				align_x = buttonsize*(0.1), # arbitrary
				anchor_y = "top",
				align_y= -buttonsize*(0.1), # arbitrary
				child = self.retour_box
			)
		)

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

	def on_draw(self):
		""" Draw this view """
		arcade.start_render()
		self.texture.draw_sized(self.window.width / 2, self.window.height / 2, self.window.width, self.window.height)
		self.manager.draw()

	def on_hide_view(self) :
		self.manager.disable()

	def add_player(self, pseudo) :
		buttonsize = self.window.width / 6 # arbitrary
		new_civil_button = OnlinePlayerButton(text=pseudo, width=buttonsize * 2, height=buttonsize / 4)
		self.players_box.add(new_civil_button.with_space_around(bottom=20))

	def remove_player(self, pseudo) :
		for button in self.players_box.children :
			if button.child.text == pseudo + " : Joueur en ligne" :
				self.players_box.remove(button)
				break

	def on_update(self, delta_time) :
		self.count += 1
		if (self.count == 30) : # changer si trop rapide ou trop long
			p = receive_string(self.window.lecture_fd, False)
			if p :
				print(p.stringify())
				match p.ID :
					case "NEW" : self.add_player(p.IO)
					case "DECO" : self.remove_player(p.IO)
					case "RES" :
						match p.IO :
							case "FOOD": self.resources[Res.FOOD] = p.PNAME
							case "WOOD": self.resources[Res.WOOD] = p.PNAME
							case "STONE": self.resources[Res.STONE] = p.PNAME
							case "GOLD": self.resources[Res.GOLD] = p.PNAME
					case "SEED" : self.seed = p.IO
					case "CR" : self.players[p.IO] = ("Joueur en ligne", p.PNAME)
					case _: print(p.stringify())
			self.count = 0
