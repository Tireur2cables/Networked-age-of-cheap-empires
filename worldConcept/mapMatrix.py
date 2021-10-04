from objects.Entity import Entity
from objects.Unit import Unit


rows, cols = (10, 10)

arr = [[0 for i in range(cols)] for j in range(rows)]


tCenter = Unit
arr[0][0] = tCenter

for row in arr:
	print(row)

