import json

with open("map/defaultmap/defaultmap.json") as json_file:
    data = json.load(json_file)
    default_map_int = data["layers"][0]["data"]
    default_map_objects_int = data["layers"][1]["data"]

int_to_type = {33:"grass", 417:"water", 577:"sand", 15:"tree", 158:"berry", 495:"stone", 111:"gold", 60:"spawn_0", 59:"spawn_1", 92: None, 91: None, 0:None}

default_map_2d = [[int_to_type[i] for i in default_map_int][i*50:(i+1)*50] for i in range(50)]

default_map_objects_2d = [[int_to_type[i] for i in default_map_objects_int][i*50:(i+1)*50] for i in range(50)]
