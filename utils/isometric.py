from utils.vector import Vector

def cart_to_iso(x, y):
	iso_x = (x - y)
	iso_y = (x + y) / 2
	return iso_x, iso_y

def iso_to_cart(iso_x, iso_y):
	x = iso_x / 2 + iso_y
	y = iso_y - iso_x / 2
	return x, y

def map_xy_to_iso(x, y, tile_width_half, tile_height_half):
	iso_x = (x - y) * tile_width_half
	iso_y = (x + y) * tile_height_half
	return iso_x, iso_y

def iso_to_map_xy(x, y, tile_width_half, tile_height_half):
	map_x = (x / tile_width_half + y / tile_height_half) / 2
	map_y = (y / tile_height_half - (x / tile_width_half)) / 2
	return map_x, map_y

def map_pos_to_iso(pos, tile_width_half, tile_height_half):
	iso_x = (pos.x - pos.y) * tile_width_half
	iso_y = (pos.x + pos.y) * tile_height_half
	return Vector(iso_x, iso_y)

def iso_to_map_pos(pos, tile_width_half, tile_height_half):
	map_x = (pos.x / tile_width_half + pos.y / tile_height_half) / 2
	map_y = (pos.y / tile_height_half - (pos.x / tile_width_half)) / 2
	return Vector(map_x, map_y)
