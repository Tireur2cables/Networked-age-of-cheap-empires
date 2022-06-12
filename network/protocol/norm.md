Un "Packet" est une classe comportant les attributs suivants : 

ID : Chaîne de caractères indiquant le type d'informations transmises dans le champ DATA

    - "NEW" / "DECO" : Connexion / Déconnexion de la salle d'attente
    - "RES" : Initialisation des ressources de départ
    - "SEED" : Transmission de la seed d'Initialisation du monde
    - "START" : Signale le lancement de la partie

    - "CREATE_UNIT" pour créer une Unité (ex.: Villageois)
    - "HARVEST" pour récolter des ressources (ex.: Récolter des pommes)
    - "MOVE_UNIT" pour déplacer une Unité
    - "BUILD" pour construire un bâtiment (classe Buildable)
    - "ATTACK" pour qu'une unité en attaque une autre 

IO : 

    - PING : Demande d'informations ou envoi d'instruction (inutilisé)
    - PONG : Réponse à demande ou Accusé réception (inutilisé)
    - DICT : Instructions imposées (principalement pour les actions in-game)

PlayerID (PNAME): Chaîne de caractères correspondant au nom du joueur dans la partie

DATA : 
Données diverses, traitées de manière conditionnelles en fonction du champ ID.
Les différentes données dans ce champ sont séparées par le caractère ';'

Un "Packet" est sérialisé dans le format suivant : ID+'\t'+IO+'\t'+PlayerID+'\t'+DATA+'\n'
Pour lire les "Packet" qui arrivent dans le tube, on sépare les données par '\n'.
Ensuite, on redivise ces données par '\t'.
Ainsi, on reconstruit tous nos paquets en assignant aux champs leurs valeurs, et en faisant une conversion de type si nécessaire.

Ensuite on enfile les paquets par ordre d'arrivée, et on les traite un par un.

Le traitement interprète le "Packet" et effectue les instructions conformément à la norme définie.
