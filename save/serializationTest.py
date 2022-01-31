# # instantiationManager
# from os import getcwd
# from pathlib import Path
# import objects.Entity
# # UTILISER PICKLE POUR LES SAUVEGARDES !!!
# # https://stackoverflow.com/questions/2047814/is-it-possible-to-store-python-class-objects-in-sqlite
# # Utiliser sqlite, pickle, ou bien les 2 ensembles, ou séparément, et pourquoi ?
# import sqlite3
# def createWorldDB(inputName):
# 	inputName += ".db"
# 	worldName = getcwd() + str(Path('/worldConcept/', inputName))

# 	currentDB = None
# 	try:
# 		conn = sqlite3.connect(worldName)
# 		print("DB Version : ", sqlite3.version)
# 	except sqlite3.Error as e:
# 		print(e)
# 	finally:
# 		if conn:
# 			conn.close()


# #createWorldDB()
# #createWorldDB("test")



###############################################
import pickle, json

from cheats import CheatsInput
def pickleSaving(game):
	save_file = "aocesave" + CheatsInput.save_suffix +'.pkl'
	data = {'players': game.players, 'model': game.game_model, 'controller': game.game_controller}
	print(f"[Saving]: {data}")
	with open(save_file,'wb') as fileDescriptor:
		pickle.dump(data, fileDescriptor)
	print(f"[Saving]: Done!")

def pickleLoading(save_name):
	save_file = "aocesave" + CheatsInput.save_suffix +'.pkl'
	print(f"[Loading]: Loading...")
	with open(save_file,'rb') as fileDescriptor:
		data = pickle.load(fileDescriptor)
		print(f"[Loaded]: Loaded")
	print(f"[Loading]: Done!")
	return data