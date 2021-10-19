# Imports
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
	def __init__(self, window, text, size, ticked=True, music=False, fullscreen=False) :
		super().__init__(texture=arcade.load_texture(textureTicked if ticked else textureEmpty), text=text, width=size, height=size)
		self.window = window
		self.ticked = ticked
		self.music = music
		self.fullscreen = fullscreen

	def on_click(self, event: arcade.gui.UIOnClickEvent) :
		print("Checkbox : ", event)

		self.texture = arcade.load_texture(textureEmpty if self.ticked else textureTicked)

		self.ticked = not self.ticked

		if self.music :
			self.window.triggerMusic()
		elif self.fullscreen :
			self.window.triggerFullscreen()
