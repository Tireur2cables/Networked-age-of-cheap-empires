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
# - Peut-on recevoir plusieurs paquets d'un coup ?
        # - Si oui, comment les traiter ?
        # - Idées : Taille en début de message, comparer avec la taille reçue, si différent, erreur.
        # - Doit-on mettre en place un checksum ?
# - Doit-on implémenter une pile de paquets pour les traiter chronologiquement ?


import os
from game import AoCE
readThis = AoCE.lecture_fd
writeThis = AoCE.ecriture_fd

class Packet():
    def __init__(self, ID, IO, PID, data):
        self.ID = ID
        self.IO = IO
        self.PID = PID
        self.data = data

def stringify(self):
    # Return a string of a packet
    # Field separator is \t
    # Packet separator is \n
    return self.ID+"\t"+self.IO+"\t"+self.PID+"\t"+self.data+"\n"

def packetify(packetString):
    packetString.split("\t")
    packetString[3].split("\n")
    return Packet(packetString[0], packetString[1], packetString[2], packetString[3][0])




def send(packetString):
    # Send the string of a packet to C handler
    if writeThis:
        os.write(writeThis, packetString.encode())
    else :
        print("[!] Error : Cannot send message. No connection to C handler.")


def receive_string():
    # receive packet string from C handler
    if readThis:
        packetString = os.read(readThis)
        return packetString
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
        case "MOVE_UNIT":
            # (Call Controller.human_order_towards_position("move", faction, iso_position):)
            # Call Controller.move_entity(entity, end_position)
            print("[<--] Received move order : " + packet.data)

        case "BUILD":
            # (Call Controller.human_order_towards_position("build", faction, iso_position):)
            # Call Controller.order_build(entity, map_position)
            # Installer une construction ou un site de construction
            print("[<--] Received build order : " + packet.data)
            pass        
        case 404:
            pass
# def forge():
    
#     pass
