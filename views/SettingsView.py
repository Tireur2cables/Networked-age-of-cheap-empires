# Imports
import arcade
from views.CustomButtons import NextViewButton, CheckboxButton

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
		buttonsize = self.window.width / 6 # arbitrary
		checkboxsize = buttonsize / 2 # arbitrary

		# Create a vertical BoxGroup to align buttons
		self.v_box = arcade.gui.UIBoxLayout()

		# Create checkboxes
		music_button = CheckboxButton(self.window, text="Musique", size=checkboxsize, ticked=self.window.isPlayingMusic(), music=True)
		self.v_box.add(music_button.with_space_around(bottom=20))

		fullscreen_button = CheckboxButton(self.window, text="Plein écran", size=checkboxsize, ticked=self.window.fullscreen, fullscreen=True)
		self.v_box.add(fullscreen_button.with_space_around(bottom=20))

		vsync_button = CheckboxButton(self.window, text="Vsync", size=checkboxsize, ticked=self.window.vsync, vsync=True)
		self.v_box.add(vsync_button.with_space_around(bottom=20))

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
		arcade.draw_text("Settings Screen", self.window.width / 2, self.window.height * 5 / 6, arcade.color.WARM_BLACK, font_size=50, anchor_x="center") # arbitrary

		self.manager.draw()


	def on_hide_view(self) :
		self.manager.disable()
