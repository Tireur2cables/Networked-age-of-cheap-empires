#from map.map import Map
from map.tile import Tile#, TileSprite

from entity.Zone import Gold, Stone, Wood #, Zone,Resources
#from map.defaultmap import default_map_2d
import noise
import numpy as np
from utils.vector import Vector

################################
# 1 generation de perlin noise #
################################
def perlin_array(size = (50, 50),
			scale=21, octaves = 50,
			persistence = 0.1,
			lacunarity = 2,
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

#perlin_array(seed=61)

def process_array(array, size = (50,50)):
	#baseTile = Tile("grass", 0,0,None)
	out = [[0 for y in range(size[1])] for x in range(size[0])]
	for x in range(size[0]):
		for y in range(size[1]):
			if array[x][y] < 0.18:
				#layer2=Stone(Vector(x,y))
				out[x][y] = Tile("grass", Vector(x, y))
			elif array[x][y] < 0.287:
				#layer2=Stone(Vector(x,y))
				out[x][y] = Tile("grass", Vector(x, y))
			elif array[x][y] < 0.315:
				#layer2=Stone(Vector(x,y))
				out[x][y] = Tile("grass", Vector(x, y))
			elif array[x][y] < 0.32:
				out[x][y] = Tile("grass", Vector(x, y),"stone")
			elif array[x][y] < 0.45:
				out[x][y] = Tile("grass", Vector(x, y))
			elif array[x][y] < 0.47:
				out[x][y] = Tile("grass", Vector(x, y),"tree")
			elif array[x][y] < 0.578:
				#layer2=Wood(Vector(x,y))
				out[x][y] = Tile("grass", Vector(x, y))
			elif array[x][y] < 0.58:
				#layer2=Wood(Vector(x,y))
				out[x][y] = Tile("grass", Vector(x, y),"gold")
			elif array[x][y] < 0.65:
				#layer2=Wood(Vector(x,y))
				out[x][y] = Tile("grass", Vector(x, y))
			elif array[x][y] < 0.75:
				#layer2=Gold(Vector(x,y))
				out[x][y] = Tile("sand", Vector(x, y))
			elif array[x][y] < 0.755:
				#layer2=Gold(Vector(x,y))
				out[x][y] = Tile("sand", Vector(x, y),"gold")
			else:
				out[x][y] = Tile("water", Vector(x, y))

	#genere la sprite
	for x in range(size[0]):
		for y in range(size[1]):
			out[x][y].init_sprite()

	return out

#########################################
# plusieurs generations de perlin noise #
#########################################
def perlin_array2(size = (50, 50),
			scale=21, octaves = 50,
			persistence = 0.1,
			lacunarity = 2,
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
	return arr

def process_array2(size = (50,50), seed=None, nbr_players=1):
	#baseTile = Tile("grass", 0,0,None)
	# default => grass everywhere
	out = [[Tile("grass", Vector(x, y)) for y in range(size[1])] for x in range(size[0])]
	if seed is None:
		seed = np.random.randint(0, 100)
		print("seed was {}".format(seed))

	# layer 1 => ground
	array = perlin_array2(size=size, seed=seed)
	for x in range(size[0]):
		for y in range(size[1]):
			if array[x][y] < 0.67:
				#grass by default
				pass
			elif array[x][y] < 0.75:
				out[x][y].blockID = "sand"
			else:
				out[x][y].blockID = "water"
				out[x][y].is_free = 0

	# layer 2 => ressources
	#trees
	seed = (seed+5)%100
	array = perlin_array2(size=size, seed=seed, octaves=20, scale=8)
	for x in range(size[0]):
		for y in range(size[1]):
			if array[x][y] > 0.75 and out[x][y].blockID != "water":
				out[x][y].pointer_to_entity = "tree"

	#gold
	seed = (seed+5)%100
	array = perlin_array2(size=size, seed=seed, octaves=20, scale=4)
	for x in range(size[0]):
		for y in range(size[1]):
			if array[x][y] > 0.87 and out[x][y].blockID != "water":
				out[x][y].pointer_to_entity = "gold"

	#stone
	seed = (seed+5)%100
	array = perlin_array2(size=size, seed=seed, octaves=20, scale=4)
	for x in range(size[0]):
		for y in range(size[1]):
			if array[x][y] > 0.89 and out[x][y].blockID != "water":
				out[x][y].pointer_to_entity = "stone"

	#finding somewhere to put TownCenter
	# nbofFreeTiles=0
	zoneSize=6
	# stop=0

	# for x in range(size[0]):
	# 	if stop == 1:
	# 			break
	# 	for y in range(size[1]):
	# 		if stop == 1:
	# 			break
	# 		nbofFreeTiles=0
	# 		for a in range(x,x+zoneSize):
	# 			for b in range(y,y+zoneSize):
	# 				if out[a][b].blockID == "water":
	# 					nbofFreeTiles=0
	# 					continue
	# 				else:
	# 					nbofFreeTiles+=1
	# 		if nbofFreeTiles==zoneSize*zoneSize:
	# 			towncenterpos=Vector(x,y)
	# 			stop=1


	if nbr_players > 0:
		for a in range(10,10+zoneSize):
			for b in range(10,10+zoneSize):
				out[a][b].blockID = "grass"
				out[a][b].pointer_to_entity = None

		out[11][11].pointer_to_entity = "spawn_0"

		for a in range(9,9+zoneSize+2,zoneSize+1):
			for b in range(9,9+zoneSize+2,zoneSize+1):
				out[a][b].blockID = "grass"
				out[a][b].pointer_to_entity = "berry"



	if nbr_players > 1:
		for a in range(size[0]-10,size[0]-10+zoneSize):
			for b in range(size[1]-10,size[1]-10+zoneSize):
				out[a][b].blockID = "grass"
				out[a][b].pointer_to_entity = None
				#if (((a==size[0]-10) or (a==size[0]-10+zoneSize)) and ((b==size[1]-10) or (b==size[1]-10+zoneSize))):

		out[size[0]-10+1][size[1]-10+1].pointer_to_entity = "spawn_1"

		for a in range(size[0]-11,size[0]-10+zoneSize+2,zoneSize+1):
			for b in range(size[0]-11,size[0]-10+zoneSize+2,zoneSize+1):
				out[a][b].blockID = "grass"
				out[a][b].pointer_to_entity = "berry"





	if nbr_players > 2:
		for a in range(10,10+zoneSize):
			for b in range(size[1]-10,size[1]-10+zoneSize):
				out[a][b].blockID = "grass"
				out[a][b].pointer_to_entity = None
				#if (((a==size[0]-10) or (a==size[0]-10+zoneSize)) and ((b==size[1]-10) or (b==size[1]-10+zoneSize))):

		out[10+1][size[1]-10+1].pointer_to_entity = "spawn_2"

		for a in range(9,9+zoneSize+2,zoneSize+1):
			for b in range(size[0]-11,size[0]-10+zoneSize+2,zoneSize+1):
				out[a][b].blockID = "grass"
				out[a][b].pointer_to_entity = "berry"


	if nbr_players > 3:
		for b in range(10,10+zoneSize):
			for a in range(size[1]-10,size[1]-10+zoneSize):
				out[a][b].blockID = "grass"
				out[a][b].pointer_to_entity = None
				#if (((a==size[0]-10) or (a==size[0]-10+zoneSize)) and ((b==size[1]-10) or (b==size[1]-10+zoneSize))):

		out[size[1]-10+1][10+1].pointer_to_entity = "spawn_3"

		for b in range(9,9+zoneSize+2,zoneSize+1):
			for a in range(size[0]-11,size[0]-10+zoneSize+2,zoneSize+1):
				out[a][b].blockID = "grass"
				out[a][b].pointer_to_entity = "berry"



	# genere la sprite
	for x in range(size[0]):
		for y in range(size[1]):
			out[x][y].init_sprite()

	return out


#a = process_array(perlin_array())
#print(a)


# tileArray = [[Tile("grass",x,y,None) for y in range(50)] for x in range(50)]
# print(tileArray)

# for x in range(50):
#     for y in range(50):
#         noise.pnoise2(x/scale, y/scale, octaves=octaves, persistence=persistence, lacunarity=lacunarity, repeatx=1024, repeaty=1024, base=seed)

#         tileArray[x][y]=Tile()
