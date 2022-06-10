# PYtoC : Python to C data converter for AOCE
# Roadmap:
# 	- Add support for seed-sending DONE
# 	- Add support for sending coordinates to place a Buildable DONE
# 	- Add support for sending coordinates to move a Unit DONE
# 	- Add support for checksum and error-handling
# 	- Add support for sending orders to the C handler
# 	- Add support for sending a list of instructions to interpret
#


# QUESTIONS POUR BATTAGLINI :
# - Peut-on recevoir plusieurs paquets d'un coup ? OUI
        # - Si oui, comment les traiter ? File / Rappeler la fonction si début paquet
        # - Idées : Taille en début de message, comparer avec la taille reçue, si différent, continuer de lire.
        # - Doit-on mettre en place un checksum ? OUI Comment le faire ?
# - Doit-on implémenter une file de paquets pour les traiter chronologiquement ? OUI
# Faire ça tous les X "on_update", et les traiter dans l'ordre de la file,

import os





class Packet():
	def __init__(self, ID, IO, PNAME, data):
		self.ID = ID
		self.IO = IO
		self.PNAME = PNAME
		self.data = data

	def stringify(self):
		# Return a string of a packet
		# Field separator is \t
		# Packet separator is \n
		return self.ID+"\t"+self.IO+"\t"+self.PNAME+"\t"+self.data+"\n"

def packetify(packetString):
	tab = str(packetString).split("\t")
	diff = 4 - len(tab)
	for i in range(max(diff, 0)) :
		tab.append("")
	return Packet(tab[0], tab[1], tab[2], tab[3])




def send(packetString, writeDesc):
	# Send the string of a packet to C handler
	if writeDesc:
		os.write(writeDesc, packetString.encode())
		print("Packet sent : " + packetString)
	else :
		print("[!] Error : Cannot send message. No connection to C handler.")


def receive_string(readDesc, block = True):
    # receive packet string from C handler
	if readDesc:
		if len(packetQueue) > 0 :
			return packetQueue.pop(0)
		else :
			try :
				packetString = ""
				while len(packetString) == 0 or packetString[-1] != "\n" :
					#print("ici : " + packetString)
					packetString += os.read(readDesc, 512).decode()
					if len(packetString) == 0 and not block :
						break
				if len(packetString) > 0 :
					s = packetString.split("\n")
					for p in s :
						packetQueue.append(packetify(p))
					return packetQueue.pop(0)
				else :
					return packetString

			except OSError as e:
				pass
	else :
		print("[!] Error : Cannot receive message. No connection to C handler.")

def interpret(packet):
	# Interpret the packet and return a list of instructions
	match packet.ID:

		case "SEED":
			# Call Game.setup() and View.setup(), sending seed as arg
			seed=packet.data
			print("[<--] Received seed : " + seed)
			# AoCE.setup(seed)

		case "CREATE_UNIT":
            # jdis ptet de la d mais pour moi c'est
            # on call add_entity_to_game() from controller.py
			print("[<--] Received unit : " + packet.data)

			pass

		case "HARVEST":
            # order_harverst() from controller.py
			#SYNTAXE : Packet("HARVEST","DICT",self.game.window.pseudo, (entity.iso_position + ";" + str(aimed_tile.grid_position)))


			pass

		case "MOVE_UNIT":
			# (Call Controller.human_order_towards_position("move", faction, iso_position):)
			# Call Controller.move_entity(entity, end_position)
			# Structure of packet.data :
			#   - faction
			#   - iso_position
			#   - entity : Use tuple in Game.get_units_by_id()
			#   - end_position
			datatab = packet.data.split(";")
			start_x=datatab[0]
			start_y=datatab[1]
			end_x=datatab[2]
			end_y=datatab[3]
			# entity=datatab[4]
			Controller.find_entity_in_sprites()
			#Controller.move_entity(entity, end)

			# SYNTAXE : send((Packet("MOVE_UNIT","DICT",self.game.window.pseudo, (entity.iso_position + ";" + str(end_grid_position)))).stringify(),self.game.window.ecriture_fd)

			print("[<--] Received move order : X =" + start_x + " Y = " + start_y + " -> X = " + end_x + " Y = " + end_y)


		case "BUILD":
			# (Call Controller.human_order_towards_position("build", faction, iso_position):)
			# Call Controller.order_build(entity, map_position)
			# Installer une construction ou un site de construction
			# Structure of packet.data :
			#   - faction
			#   - iso_position

			# SYNTAXE : send((Packet("BUILD","DICT",self.game.window.pseudo, str(entity.iso_position + ";" + str(map_position)+";"+str(building_name)))).stringify(),self.game.window.ecriture_fd)			#avec les entity.pos communiquées, on retrouve les bonnes unités en parcourant le tableau des entities
			#DATA : map_pos et building_name séparés par une tabulation

			print("[<--] Received build order : " + packet.data)


		case "ATTACK":
			# SYNTAXE : send((Packet("ATTACK","DICT",self.game.window.pseudo, str(entity.iso_position+"\t"+aimed_entity.iso_position))).stringify(),self.game.window.ecriture_fd)

			print("[<--] Received build order : " + packet.data)

packetQueue = []

# paquetdemerde = Packet("ID", "IO", "0", "TEMALATAILLEDELADATA")


# paquetdemerde1= Packet("ID", "IO", "1", "TEMALATAILLEDELADATA")
# paquetdemerde2= Packet("ID", "IO", "2", "TEMALATAILLEDELADATA")
# packetQueue.insert(-1,paquetdemerde)
# packetQueue.insert(-1,paquetdemerde1)
# packetQueue.insert(-1,paquetdemerde2)

# packet = packetQueue.pop()
# packet = packetQueue.pop()
# packet = packetQueue.pop()
# print(len(packetQueue))
