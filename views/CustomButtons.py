# Imports
import arcade.gui
from save.serializationTest import *

# Constants
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
	def __init__(self, window, text, size, ticked=True, music=False, fullscreen=False) :
		super().__init__(texture=arcade.load_texture(textureTicked if ticked else textureEmpty), text=text, width=size, height=size)
		self.window = window
		self.ticked = ticked
		self.music = music
		self.fullscreen = fullscreen

	def on_click(self, event: arcade.gui.UIOnClickEvent) :
		self.texture = arcade.load_texture(textureEmpty if self.ticked else textureTicked)

		self.ticked = not self.ticked

		if self.music :
			self.window.triggerMusic()
		elif self.fullscreen :
			self.window.triggerFullscreen()

class ConstructButton(arcade.gui.UITextureButton) :
	def __init__(self,image, construct, width=60, height=90, text=""):
		super().__init__(texture = arcade.load_texture(image),width=width, height=height, text=text)
		self.image = image
		self.construct = construct

	def on_click(self, event: arcade.gui.UIOnClickEvent):
		self.construct
		print("Lezgo mon soleil")
