# CE FICHIER EST INDEPENDANT DU PROJET

import noise
import numpy as np
import arcade
import random

shape = (5,5)
scale = 10.0  # "Définition", "Pixelisation", ...
octaves = 6  # Taux de détail (différence entre chaque case, sinon ça fait une tache presque d'une seule couleur)
persistence = 0.1  # A quel point les cases sont influencées par les voisines.
lacunarity = 2.0  # Taux de détail (de + en + chaotique) : plus ça va plus la forme géométrique du bruit est complexe (forme de "fractale").
seed = random.randint(0, 100)  # Pour être modifié en fonction du menu.
def show_map(array):
	print("\nShowing the map :")
	for i in range(shape[0]):
		for j in range(shape[1]):
			print(round(array[i][j], 4), end='\t')
		print()

world = [[0 for j in range(shape[1])] for i in range(shape[0])]
# for i in range(shape[0]):
#     for j in range(shape[1]):
#         pass
# show_map(world)



# --- Constants ---
SPRITE_SCALING = 1

ROWS = 50
COLUMNS = 80

CELL_WIDTH = 16
CELL_HEIGHT = 16
MARGIN = 3

SCREEN_WIDTH = (CELL_WIDTH + MARGIN) * COLUMNS + MARGIN
SCREEN_HEIGHT = (CELL_HEIGHT + MARGIN) * ROWS + MARGIN

SCREEN_TITLE = "Test"
PEAR_WHITE = (255, 255, 255)
PEAR_BLACK = (39, 39, 54)
PEAR_RED = (235, 86, 75)


class MyGame(arcade.Window):

	def __init__(self):
		""" Initializer """
		super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=False)
		self.grid_sprite_list = arcade.SpriteList()
		self.grid = []

		print("\nShowing the map :")
		for row in range(ROWS):
			self.grid.append([])
			for column in range(COLUMNS):
				x = column * (CELL_WIDTH + MARGIN) + (CELL_WIDTH / 2 + MARGIN)
				y = row * (CELL_HEIGHT + MARGIN) + (CELL_HEIGHT / 2 + MARGIN)
				cell = MyGame.create_cell(row, column)
				print(round(((cell+1)/2), 4), end='\t')
				entity = Cell(None, cell)
				entity.center_x = x
				entity.center_y = y
				self.grid_sprite_list.append(entity)
				self.grid[row].append(entity)
			print()


		arcade.set_background_color(PEAR_BLACK)
		self.set_mouse_visible(True)

	@staticmethod
	def create_cell(x, y):
		return noise.pnoise2(x/scale, y/scale, octaves=octaves, persistence=persistence, lacunarity=lacunarity, repeatx=1024, repeaty=1024, base=seed)

	def on_draw(self):
		arcade.start_render()
		self.grid_sprite_list.draw()


class Cell(arcade.SpriteSolidColor):
	def __init__(self, color, p_noise):
		# color_p_noise = int(((p_noise+1)/2)*255)
		color_p_noise = int(p_noise * 255)
		if p_noise < 0.3:
			p_noise_t = (0, 255, 0)
		else:
			p_noise_t = (0, 0, 255)
		print(p_noise_t)
		super().__init__(CELL_WIDTH, CELL_HEIGHT, p_noise_t)




def main():
	""" Main method """
	game = MyGame()
	arcade.run()


if __name__ == "__main__":
	main()


# https://medium.com/@yvanscher/playing-with-perlin-noise-generating-realistic-archipelagos-b59f004d8401
