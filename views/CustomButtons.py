# Imports
from ctypes import string_at
from arcade.arcade_types import Color
import arcade.gui
from save.serializationTest import *

# Constants
from CONSTANTS import Resource as Res
textureTicked = "Ressources/img/tick.png"
textureEmpty = "Ressources/img/empty.png"

#############################################################
#					Custom buttons							#
#############################################################

# Button to exit the game
class QuitButton(arcade.gui.UIFlatButton) :
	def __init__(self, window, text, width) :
		super().__init__(text=text, width=width)
		self.window = window

	def on_click(self, event: arcade.gui.UIOnClickEvent) :
		self.window.exit()


class SaveButton(arcade.gui.UIFlatButton) :
	def __init__(self, unit_list, tile_list, zone_list, text, width) :
		super().__init__(text=text, width=width)
		self.unit_list = unit_list
		self.tile_list = tile_list
		self.zone_list = zone_list

	def on_click(self, event: arcade.gui.UIOnClickEvent) :
		pickleSaving("savetest",self.unit_list,self.tile_list,self.zone_list)

# Button to return to the main menu
class NextViewButton(arcade.gui.UIFlatButton) :
	def __init__(self, window, nextView, text, width) :
		super().__init__(text=text, width=width)
		self.window = window
		self.nextView = nextView

	def on_click(self, event: arcade.gui.UIOnClickEvent) :
		self.nextView.setup()
		self.window.show_view(self.nextView)

# Button to return to the main menu
class LaunchGameButton(arcade.gui.UIFlatButton) :
	def __init__(self, window, nextView, pregameview, text, width) :
		super().__init__(text=text, width=width)
		self.window = window
		self.nextView = nextView
		self.pregameview = pregameview

	def on_click(self, event: arcade.gui.UIOnClickEvent) :
		ia = {}
		for padding in self.pregameview.ia_box.children :
			name, diff = padding.child.text.split(padding.child.sep)
			ia[name] = diff

		ressources = {}
		tab = [Res.GOLD, Res.WOOD, Res.FOOD, Res.STONE]
		indice = 0
		for texture_pane in self.pregameview.name_input_ressources :
			ressources[tab[indice]] = texture_pane.child.text
			indice += 1
		self.nextView.setup(ressources, ia, self.pregameview.isPlayer)
		self.window.show_view(self.nextView)

# Button to display things or not
class ListButton(arcade.gui.UIFlatButton) :
	def __init__(self, vbox, children, text, width) :
		super().__init__(text=text, width=width)
		self.vbox = vbox
		self.list = children
		self.isDisplayed = False

	def on_click(self, event: arcade.gui.UIOnClickEvent) :
		self.isDisplayed = not self.isDisplayed
		self.vbox.clear()
		self.vbox.add(self)

		if self.isDisplayed :
			for child in self.list :
				self.vbox.add(child)


# CheckboxButton
class CheckboxButton(arcade.gui.UITextureButton) :
	def __init__(self, window, text, size, ticked=True, music=False, fullscreen=False, vsync=False) :
		super().__init__(texture=arcade.load_texture(textureTicked if ticked else textureEmpty), text=text, width=size, height=size)
		self.window = window
		self.ticked = ticked
		self.music = music
		self.fullscreen = fullscreen
		self.vsync = vsync

	def on_click(self, event: arcade.gui.UIOnClickEvent) :
		self.texture = arcade.load_texture(textureEmpty if self.ticked else textureTicked)

		self.ticked = not self.ticked

		if self.music :
			self.window.triggerMusic()
		elif self.fullscreen :
			self.window.triggerFullscreen()
		elif self.vsync :
			self.window.triggerVsync()

# Selection de sa difficulté
class SelctDifButton(arcade.gui.UIFlatButton):
	def __init__(self, text, size, name):
		super().__init__(text=text + " : Facile ", width=size * 2, height=size / 4)
		self.count = 0
		self.name = name
		self.list = ["Facile", "Moyen", "Difficile"]
		self.sep = " : "

	def on_click(self, event: arcade.gui.UIOnClickEvent):
		if self.count == len(self.list) - 1 :
			self.count = 0
		else :
			self.count = self.count + 1
		self.text = self.name + self.sep + self.list[self.count]

class PlayerButton(arcade.gui.UIFlatButton):
	def __init__(self, text, width, height):
		super().__init__(text=text + " : Joueur Humain", width=width, height=height)
		self.sep = " : "

class NumInput(arcade.gui.UIInputText) :
	def __init__(self, x, y, text, width, height, text_color) :
		super().__init__(x=x, y=y, text=text, width=width, height=height, text_color=text_color)

	def on_event(self, event) :
		if self._active and isinstance(event, arcade.gui.events.UITextEvent) and not (event.text.isnumeric() or event.text == "") :
			pass

		else :
			super().on_event(event)

		if self.text == "" :
			self.caret.on_text("0")

class ConstructButton(arcade.gui.UITextureButton) :
	def __init__(self,image, construct, width=60, height=90, text=""):
		super().__init__(texture = arcade.load_texture(image),width=width, height=height, text=text)
		self.image = image
		self.construct = construct

	def on_click(self, event: arcade.gui.UIOnClickEvent):
		self.construct
		print("Lezgo mon soleil")
