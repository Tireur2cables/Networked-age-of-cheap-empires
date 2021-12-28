# instantiationManager
from os import getcwd
from pathlib import Path
import objects.Entity
# UTILISER PICKLE POUR LES SAUVEGARDES !!!
# https://stackoverflow.com/questions/2047814/is-it-possible-to-store-python-class-objects-in-sqlite
# Utiliser sqlite, pickle, ou bien les 2 ensembles, ou séparément, et pourquoi ?
import sqlite3
def createWorldDB(inputName):
	inputName += ".db"
	worldName = getcwd() + str(Path('/worldConcept/', inputName))

	currentDB = None
	try:
		conn = sqlite3.connect(worldName)
		print("DB Version : ", sqlite3.version)
	except sqlite3.Error as e:
		print(e)
	finally:
		if conn:
			conn.close()


#createWorldDB()
#createWorldDB("test")
