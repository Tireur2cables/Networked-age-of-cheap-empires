# Imports
from ctypes import string_at
from arcade.arcade_types import Color
import arcade.gui

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

# Button to return to the main menu
class NextViewButton(arcade.gui.UIFlatButton) :
	def __init__(self, window, nextView, text, width) :
		super().__init__(text=text, width=width)
		self.window = window
		self.nextView = nextView

	def on_click(self, event: arcade.gui.UIOnClickEvent) :
		print("NextView :", event)
		self.nextView.setup()
		self.window.show_view(self.nextView)

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
		print("Checkbox : ", event)

		self.texture = arcade.load_texture(textureEmpty if self.ticked else textureTicked)

		self.ticked = not self.ticked

		if self.music :
			self.window.triggerMusic()
		elif self.fullscreen :
			self.window.triggerFullscreen()
		elif self.vsync :
			self.window.triggerVsync()

# Selection de sa civilisation (meme si on aura pas forcement autant de civilisation) //Inutile, on a besoin que d'une seule civilisation
class SelctCivilButton(arcade.gui.UIFlatButton):
	def __init__(self, window, text, size,name):
		super().__init__(text= text, width=size*2, height=size/4)
		self.window =window
		self.count=0
		self.name=name

	def on_click(self, event: arcade.gui.UIOnClickEvent):
		if (self.count==4):
			self.count = 0
		else :
			self.count = self.count +1

		if (self.count==0):
			self.text= self.name + " : Romains "
		elif (self.count==1):
			self.text= self.name + " : Egyptiens "
		elif (self.count==2):
			self.text= self.name + " : Gaulois "
		elif (self.count==3):
			self.text= self.name + " : Vikings "
		else :
			self.text= self.name + " : GuiLeDavien "

class NumInput(arcade.gui.UIInputText) :
	def __init__(self, x, y, text, width, height, text_color) :
		super().__init__(x=x, y=y, text=text, width=width, height=height, text_color=text_color)

	def on_event(self, event) :
		if self._active and isinstance(event, arcade.gui.events.UITextEvent) and not (event.text.isnumeric() or event.text == "") :
			pass

		else :
			super().on_event(event)
