from objects.Entity import Entity
from objects.Unit import Unit, Villager
import arcade
from utils.vector import Vector

rows, cols = (10, 10)




vill = Villager(0,0)
lol = True

#
##
###	Documentation de l'array
###	(blockId, pointerToEntity, isLocked)
##	Position : 
##
#
vill.set_position(Vector(0,0))
arr = [[(0,None,False) for i in range(cols)] for j in range(rows)]

arr[(vill.get_position()).x][(vill.get_position()).y] = (0,vill,False)
while lol:
	arr[vill.get_position().x][vill.get_position().y] = (0,None,False)
	vill.set_position(Vector(vill.get_position().x + 1,vill.get_position().y))
	vill.set_position(Vector(vill.get_position().x,vill.get_position().y + 1))
	arr[vill.get_position().x][vill.get_position().y] = (0,vill,False)
	for row in arr:
		print(row)
	print("\n\n")
	if vill.get_position().x == 9:
		lol = False
# Problème : Toujours présent à d'autres cases & donc gestion d'UID nécessaire !
# Solution temporaire : Clean la map à chaque tour de gameloop
# Avec systeme position Unit(Vector(2, 3), ...)
# v.getposition().x