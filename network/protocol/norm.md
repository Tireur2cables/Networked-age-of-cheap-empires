Logic of Game Commands : 
    X) Hello, I am Player1, I want to interact with Villager.1234, who owns this ?
    X) Hello, I am Player2, i own Villager.1234.

X) I am Player1, requesting contract on Villager.1234
X) I am Player2, leaving you contract on Villager.1234

    5) I am Player1,acknowledge contract on X for 10sec
    Actions...
    6) I am Player1,finished contract on X for 10sec



ID : 

0-9 : Service Information
0 : Client Disconnect
1 : Client Subscription : First packet sent to the already connected clients, clients answer with their clientID; We take the lowest, non taken number between 1 and 4.
2 : Ready to start game (synchronized and received game seed & map position)
3 : Map Seed Transmission
4 : 

10-19 : Basic Actions
10 : Moving Unit
11 : Placing a Buildable
12 : 


IO : 
PING : Asking for infos (service info)
PONG : Answering (service info)
DICT : Dictator infos (in-game)

PlayerID:
Between 1 and 4

DATA : 
Déviation des infos d'actions effectutées par le client et envoi sur le réseau