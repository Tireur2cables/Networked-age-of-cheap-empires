# Imports
import arcade.gui

# Constants
textureTicked = "img/tick.png"
textureEmpty = "img/empty.png"

#############################################################
#					Custom buttons							#
#############################################################

# Button to exit the game
class QuitButton(arcade.gui.UIFlatButton) :
	def on_click(self, event: arcade.gui.UIOnClickEvent) :
		arcade.exit()

# Button to return to the main menu
class NextViewButton(arcade.gui.UIFlatButton) :
	def __init__(self, window, nextView, text, width) :
		super().__init__(text=text, width=width)
		self.window = window
		self.nextView = nextView

	def on_click(self, event: arcade.gui.UIOnClickEvent) :
		print("NextView :", event)
		self.window.show_view(self.nextView)


# CheckboxButton
class CheckboxButton(arcade.gui.UITextureButton) :
	def __init__(self, window, text, size) :
		super().__init__(texture=arcade.load_texture(textureTicked), text=text, width=size, height=size)
		self.window = window
		self.ticked = True

	def on_click(self, event: arcade.gui.UIOnClickEvent) :
		print("Checkbox : ", event)
		if self.ticked :
			self.texture = arcade.load_texture(textureEmpty)
			self.ticked = False
		else :
			self.texture = arcade.load_texture(textureTicked)
			self.ticked = True
