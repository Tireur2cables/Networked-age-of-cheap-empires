#DO NOT NAME FILES LIKE PACKAGES !

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
import numpy as np # Just for random matrix

map_size=50

matrix = [[1 for y in range(map_size)] for x in range(map_size)]


N = 50
p = 0.1
mask = np.empty((N, N))
for i in range (N):
     mask[i] = np.random.choice(a=[0, 1], size=N, p=[p, 1-p])            
     if (i % 100 == 0):
          print(i)
print(mask)
grid = Grid(matrix=mask)

start = grid.node(0, 0) #Where our Entity is
end = grid.node(49, 49) # Where our entity wants to go

finder = AStarFinder(diagonal_movement=DiagonalMovement.always) # We allow movements in a diagonal
path, runs = finder.find_path(start, end, grid)

print('operations:', runs, 'path length:', len(path))
print(path) # Table of coordinate tuples, so that we know where to go
print(grid.grid_str(path=path, start=start, end=end))


		# for i in self.selection:
		# 	entity = i.entity
		# 	grid = Grid(matrix=self.pathfinding_matrix)
		# 	finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
		# 	startvec = iso_to_map_pos(entity.position, TILE_WIDTH//2, TILE_HEIGHT//2)
		# 	endvec = iso_to_map_pos(mouse_position, TILE_WIDTH//2, TILE_HEIGHT//2)
		# 	start = grid.node(startvec.int().x, startvec.int().y)
		# 	end = grid.node(endvec.int().x, endvec.int().y)
		# 	path, runs = finder.find_path(start, end, grid)
		# 	# The following calculation is necessary to have uniform speeds :
		# 	for y in path:
		# 		entity.aim_towards(Vector(y[0],y[1]), entity.speed * ((mouse_position - entity.position).normalized()))