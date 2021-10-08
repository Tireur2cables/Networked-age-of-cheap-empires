from objects.Entity import Entity
from objects.Unit import Unit, Villager
import arcade

rows, cols = (10, 10)




vill = Villager(0,0)
lol = True
arr = [[(0,None) for i in range(cols)] for j in range(rows)]
arr[vill.get_x()][vill.get_y()] = (0,vill)
while lol:
	arr[vill.get_x()][vill.get_y()] = (0,None)
	vill.set_x(vill.get_x() + 1)
	vill.set_y(vill.get_y() + 1)
	arr[vill.get_x()][vill.get_y()] = (0,vill)
	for row in arr:
		print(row)
	print("\n\n")
	if vill.get_x() == 9:
		lol = False
# Problème : Toujours présent à d'autres cases & donc gestion d'UID nécessaire !
# Solution temporaire : Clean la map à chaque tour de gameloop
# Avec systeme position Unit(Vector(2, 3), ...)
#v.getposition().x