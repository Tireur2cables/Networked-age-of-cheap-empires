# Imports
import arcade.gui

#############################################################
#					Custom buttons							#
#############################################################

# Button to exit the game
class QuitButton(arcade.gui.UIFlatButton):
	def on_click(self, event: arcade.gui.UIOnClickEvent):
		arcade.exit()

# Button to return to the main menu
class NextViewButton(arcade.gui.UIFlatButton):
	def __init__(self, window, nextView, text, width):
		super().__init__(text=text, width=width)
		self.window = window
		self.nextView = nextView

	def on_click(self, event: arcade.gui.UIOnClickEvent):
		print("NextView :", event)
		self.window.show_view(self.nextView)
