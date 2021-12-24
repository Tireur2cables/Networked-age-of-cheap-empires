from utils.vector import Vector

def cart_to_iso(x, y):
	iso_x = (x - y)
	iso_y = (x + y) / 2
	return iso_x, iso_y

def grid_xy_to_iso(x, y, tile_width_half, tile_height_half):
	iso_x = (x - y) * tile_width_half
	iso_y = (x + y) * tile_height_half
	return iso_x, iso_y

def iso_to_grid_xy(x, y, tile_width_half, tile_height_half):
	map_x = (x / tile_width_half + y / tile_height_half) / 2
	map_y = (y / tile_height_half - (x / tile_width_half)) / 2
	return int(map_x), int(map_y)

def grid_pos_to_iso(pos, tile_width_half, tile_height_half):
	iso_x = (pos.x - pos.y) * tile_width_half
	iso_y = (pos.x + pos.y) * tile_height_half
	return Vector(iso_x, iso_y)

def iso_to_grid_pos(pos, tile_width_half, tile_height_half):
	grid_x = (pos.x / tile_width_half + pos.y / tile_height_half) / 2
	grid_y = (pos.y / tile_height_half - (pos.x / tile_width_half)) / 2
	return Vector(grid_x, grid_y).int()