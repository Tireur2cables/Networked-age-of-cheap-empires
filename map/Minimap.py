# IMPORTS
import arcade
from utils.isometric import cart_to_iso
from math import sqrt

# CONSTANTS
BORDER_MINI_RECTANGLE = 15
WHITE = (255, 255, 255)
#MINIMAP_BACKGROOUND_COLOR = arcade.color.GRAY

class Minimap() :
	def __init__(self, view, default_map_size, tile_width, tile_height,	bakcground_color):
		self.view = view
		self.map_width = default_map_size * tile_width
		self.map_height = default_map_size * tile_height
		self.background_color = bakcground_color


		MINIMAP_WIDTH = int(self.view.game.window.width * 3 / 10) # arbitrary
		MINIMAP_HEIGHT = int(self.view.game.window.height * 1 / 4) # arbitrary

		self.size = (MINIMAP_WIDTH, MINIMAP_HEIGHT)

		# Texture and associated sprite to render our minimap to
		self.texture = arcade.Texture.create_empty("minimap_texture", self.size)
		self.sprite = arcade.Sprite(
			center_x=MINIMAP_WIDTH / 2,
			center_y=MINIMAP_HEIGHT / 2,
			texture=self.texture
		)

		# List of all our minimaps (there's just one)
		self.sprite_list = arcade.SpriteList()
		self.sprite_list.append(self.sprite)

		self.selected = False

	def update_minimap(self) :
		iso_width, iso_height = cart_to_iso(self.map_width, self.map_height)
		proj = -iso_width, iso_width, 0, iso_height - self.view.camera.viewport_height * 3 / 4 # it works
		with self.sprite_list.atlas.render_into(self.texture, projection=proj) as fbo:
			fbo.clear(self.background_color)
			self.view.tile_sprite_list.draw()
			self.view.zone_sprite_list.draw()
			self.view.entity_sprite_list.draw()
			top_left_x = self.view.camera_x + self.view.camera.viewport_width / 2
			top_left_y = self.view.camera_y + self.view.camera.viewport_height / 2
			arcade.draw_rectangle_outline(top_left_x, top_left_y, self.view.camera.viewport_width, self.view.camera.viewport_height, WHITE, BORDER_MINI_RECTANGLE)

	def draw(self) :
		self.update_minimap()
		# Draw the minimap
		self.sprite_list.draw()

	def is_on_minimap_sprite(self, x, y) :
		return (0 <= x <= self.size[0]) and (0 <= y <= self.size[1])
