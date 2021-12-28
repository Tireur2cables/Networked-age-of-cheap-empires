from map.map import Map
from map.tile import Tile, TileSprite

from entity.Zone import Zone
from map.defaultmap import default_map_2d
import noise
import numpy as np


def perlin_array(size = (50, 50),
			scale=75, octaves = 50, 
			persistence = 0.3, 
			lacunarity = 2.0, 
			seed = None):

	if not seed:

		seed = np.random.randint(0, 100)
		print("seed was {}".format(seed))

	arr = np.zeros(size)
	for i in range(size[0]):
		for j in range(size[1]):
			arr[i][j] = noise.pnoise2(i / scale,
										j / scale,
										octaves=octaves,
										persistence=persistence,
										lacunarity=lacunarity,
										repeatx=1024,
										repeaty=1024,
										base=seed)
	max_arr = np.max(arr)
	min_arr = np.min(arr)
	norm_me = lambda x: (x-min_arr)/(max_arr - min_arr)
	norm_me = np.vectorize(norm_me)
	arr = norm_me(arr)
	#print(arr)
	return arr

perlin_array(seed=61)

def process_array(array, size = (50,50)):
	baseTile = Tile("grass", 0,0,None)
	out = [[0 for y in range(size[1])] for x in range(size[0])]
	for x in range(size[0]):
		for y in range(size[1]):
			if array[x][y] < 0.45:
				out[x][y] = Tile("grass", x,y)
			elif array[x][y] < 0.58:
				out[x][y] = Tile("grass", x,y, "tree")
			elif array[x][y] < 0.75:
				out[x][y] = Tile("sand", x,y, "gold")
			else:
				out[x][y] = Tile("water", x,y)
	return out

#a = process_array(perlin_array())
#print(a)


# tileArray = [[Tile("grass",x,y,None) for y in range(50)] for x in range(50)]
# print(tileArray)

# for x in range(50):
#     for y in range(50):
#         noise.pnoise2(x/scale, y/scale, octaves=octaves, persistence=persistence, lacunarity=lacunarity, repeatx=1024, repeaty=1024, base=seed)

#         tileArray[x][y]=Tile()

pass