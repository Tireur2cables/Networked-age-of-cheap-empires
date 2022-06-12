# Connection à une partie :  

- l'host accepte la connection et envoi un paquet "PSEUDO XXXXX" contenant son pseudo.  

- le nouveau joueur reçoit le paquet et répond par un paquet "PSEUDO XXXXX" contenant son pseudo à lui.  

- l'host reçoit le paquet et répond soit par "FIRST" si c'est le premier nouveau joueur soit par un paquet du type "X.X.X.X X.X.X.X ..."  contenant une liste des ip des joueurs deja connectes séparé par un espace.  
