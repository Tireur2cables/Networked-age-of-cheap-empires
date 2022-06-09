#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <sys/select.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <time.h>
#include <fcntl.h>

#define ERROR -1
#define TRUE 1
#define FALSE 0
#define TUBE_SIZE 2
#define TUBE_LECT 0
#define TUBE_ECRI 1
#define PACKET_SIZE 512 // a determiner
#define PORT 1234
#define MAX_CLI 3 // 3 autres joueurs en plus de nous
#define CLOSED_CONECTION 0
#define IP_LEN 15
#define PSEUDO_LEN 20 // attention à update si on update les pseudo

typedef struct player {
	char ip[IP_LEN + 1];
	int port;
	char pseudo[PSEUDO_LEN + 1];
	int sock;
} player;

int nbdigit(int);
void close_tube(int [TUBE_SIZE]);
void error(char *);
void creer_tubes();
void launch_communication();
void launch_python();
fd_set create_set(int *);
void recuperer_packet(char [PACKET_SIZE + 1], int);
void send_packet(char [PACKET_SIZE + 1], int);
void gerer_py_mess(char [PACKET_SIZE + 1]);
void gerer_c_mess(char [PACKET_SIZE + 1], int);
void create_serv();
void handle_new_connection();
void close_serv();
void join_game();

int fd_py_to_c[TUBE_SIZE];
int fd_c_to_py[TUBE_SIZE];
int retour;
int serv_sock;
int is_serv_launched = FALSE;
int nb_cli = 0;
player players[MAX_CLI];
char pseudo[PSEUDO_LEN + 1];
int am_i_host = FALSE;

int main(int argc, char const *argv[]) {
	// initialisation du pseudo
	bzero(pseudo, PSEUDO_LEN + 1);

	// initialisation du tableau des joueurs
	memset(players, ERROR, MAX_CLI * sizeof(player));

	// initialisation des tubes
	creer_tubes();

	int pid = fork();
	switch (pid) {
		case ERROR : {
			close_tube(fd_c_to_py);
			close_tube(fd_py_to_c);
			error("Erreur lors du fork");
		}
		case 0 : launch_python();
		default : launch_communication();
	}

	return 0;
}

void launch_communication() {
	// on ferme les parties des tubes que l'on utilisera pas
	close(fd_py_to_c[TUBE_ECRI]);
	close(fd_c_to_py[TUBE_LECT]);

	printf("Programme C en attente\n");

	char buff[PACKET_SIZE + 1];

	while (TRUE) {
		// on créer l'ensembles de file descriptor sur lesquels on attends des messages
		int max_fd;
		fd_set set = create_set(&max_fd);

		retour = select(max_fd + 1, &set, NULL, NULL, NULL);
		if (retour == ERROR) {
			close(fd_py_to_c[TUBE_LECT]);
			close(fd_c_to_py[TUBE_ECRI]);
			if (is_serv_launched) close_serv();
			error("Erreur du select");
		}

		// on regarde qui veut nous envoyer un message (tube ou socket)
		if (FD_ISSET(fd_py_to_c[TUBE_LECT], &set)) {// le programme python veut envoyer un message
			recuperer_packet(buff, fd_py_to_c[TUBE_LECT]);
			gerer_py_mess(buff);
		}

		if (is_serv_launched) {
			if (FD_ISSET(serv_sock, &set)) // un nouveau joueur veut se connecter
				handle_new_connection();

			for (int i = 0; i < MAX_CLI; i++) {
				if (FD_ISSET(players[i].sock, &set)) {
					recuperer_packet(buff, players[i].sock);
					gerer_c_mess(buff, i);
				}
			}
		}
	}
}

void gerer_c_mess(char buff[PACKET_SIZE + 1], int indice) {
	// retour ici correspond au nombre de bytes reçus par recuperer_packet
	if (retour == CLOSED_CONECTION) {
		sprintf(buff, "DECO %s", players[indice].pseudo);
		send_packet(buff, fd_c_to_py[TUBE_ECRI]);
		printf("Joueur %s déconnecté...\n", players[indice].pseudo);
		close(players[indice].sock);
		players[indice].sock = ERROR;
		players[indice].pseudo[0] = '\0';
		players[indice].ip[0] = '\0';
		players[indice].port = ERROR;
		nb_cli--;
	}

	else {
		printf("message reçu : %s\n", buff);
		send_packet(buff, fd_c_to_py[TUBE_ECRI]); // envoi le message au python directement
	}
}

void gerer_py_mess(char buff[PACKET_SIZE + 1]) {
	if (strcmp(buff, "STOP") == 0) {
		printf("Je me stoppe\n");
		close(fd_py_to_c[TUBE_LECT]);
		close(fd_c_to_py[TUBE_ECRI]);
		if (is_serv_launched) close_serv();
		exit(EXIT_SUCCESS);
	}

	else if (strncmp(buff, "INIT ", 5) == 0) {
		printf("Je lance la partie réseau\n");
		if (pseudo[0] == '\0') sscanf(buff, "INIT %s", pseudo);
		printf("mon pseudo est : %s\n", pseudo);
		create_serv();
		am_i_host = TRUE;
	}

	else if (strcmp(buff, "CANCEL") == 0) {
		printf("Je cancel le serveur\n"); // normal que ce soit print au depart on desactive au setup de main view
		if (is_serv_launched) {
			close_serv();
			am_i_host = FALSE;
		}
	}

	else if (strncmp(buff, "JOIN ", 5) == 0) {
		printf("Je me connecte à la partie\n");
		char ip[IP_LEN + 1];
		//printf("Reçu: %s\n", buff);
		if (sscanf(buff, "JOIN %s %s", pseudo, ip) != 2) recuperer_packet(buff, fd_py_to_c[TUBE_LECT]);
		printf("Message reçu: %s", buff);
		printf("IP: %s\n", ip);
		join_game(ip);
		//create_serv();
	}

	else {
		for (size_t i = 0; i < MAX_CLI; i++) {
			if (players[i].sock != ERROR) {
				printf("message reçu du python : %s\n", buff);
				send_packet(buff, players[i].sock);
			}
		}
	}
}

void join_game(char ip[IP_LEN + 1]) {
	players[0].sock = socket(AF_INET, SOCK_STREAM, 0);
	if (players[0].sock == ERROR) {
		close(fd_py_to_c[TUBE_LECT]);
		close(fd_c_to_py[TUBE_ECRI]);
		close_serv();
		error("Erreur de création de la socket!");
	}
	players[0].port = PORT;
	strcpy(players[0].ip, ip);

	struct sockaddr_in serv_addr;
	socklen_t serv_size = sizeof(serv_addr);
	bzero(&serv_addr, serv_size);

	serv_addr.sin_family = AF_INET;
	serv_addr.sin_port = htons(PORT);
	serv_addr.sin_addr.s_addr = inet_addr(players[0].ip);

	printf("Connection au serveur %s sur le port %d...\n", players[0].ip, PORT);

	int retour = connect(players[0].sock, (struct sockaddr *) &serv_addr, serv_size);
	if (retour == ERROR) {
		close(fd_py_to_c[TUBE_LECT]);
		close(fd_c_to_py[TUBE_ECRI]);
		close_serv();
		error("Erreur de connection!");
	}

	printf("Connecté!\n");

	char buff[PACKET_SIZE + 1];
	recuperer_packet(buff, players[0].sock);
	sscanf(buff, "PSEUDO %s", players[0].pseudo);
	sprintf(buff, "NEW %s", players[0].pseudo);
	send_packet(buff, fd_c_to_py[TUBE_ECRI]);
	sprintf(buff, "PSEUDO %s", pseudo);
	send_packet(buff, players[0].sock);

	recuperer_packet(buff, players[0].sock);
	if (strcmp(buff, "FIRST") == 0) {
		printf("Pas besoin de se connecter à d'autres\n");
	}
	else {
		printf("Je vais me connecter à tous ces autres la :\n%s\n", buff);

		char ip1[IP_LEN+1];
		char ip2[IP_LEN+1];
		int nb = sscanf(buff, "%s %s", ip1, ip2);

		players[1].sock = socket(AF_INET, SOCK_STREAM, 0);
		if (players[1].sock == ERROR) {
			close(fd_py_to_c[TUBE_LECT]);
			close(fd_c_to_py[TUBE_ECRI]);
			close_serv();
			error("Erreur de création de la socket!");
		}
		players[1].port = PORT;
		strcpy(players[1].ip, ip1);
		struct sockaddr_in serv_addr;
		socklen_t serv_size = sizeof(serv_addr);
		bzero(&serv_addr, serv_size);
		serv_addr.sin_family = AF_INET;
		serv_addr.sin_port = htons(PORT);
		serv_addr.sin_addr.s_addr = inet_addr(players[1].ip);

		if (nb == 1) {
			int connexion = connect(players[1].sock, (struct sockaddr *) &serv_addr, serv_size);
			if (connexion == ERROR) {
				close(fd_py_to_c[TUBE_LECT]);
				close(fd_c_to_py[TUBE_ECRI]);
				close_serv();
				error("Erreur de connection!");
			}
			else {
				printf("Connecté à l'autre joueur !\n");
				char buff[PACKET_SIZE + 1];
				recuperer_packet(buff, players[1].sock);
				sscanf(buff, "PSEUDO %s", players[1].pseudo);
				sprintf(buff, "PSEUDO %s", pseudo);
				send_packet(buff, players[1].sock);
				printf("Pseudo du joueur 1: %s\n", players[1].pseudo);
				sprintf(buff, "NEW %s", players[1].pseudo);
				send_packet(buff, fd_c_to_py[TUBE_ECRI]);
			}
		}
		else if (nb > 1) {
			players[2].sock = socket(AF_INET, SOCK_STREAM, 0);
			if (players[2].sock == ERROR) {
				close(fd_py_to_c[TUBE_LECT]);
				close(fd_c_to_py[TUBE_ECRI]);
				close_serv();
				error("Erreur de création de la socket!");
			}
			players[2].port = PORT;
			strcpy(players[2].ip, ip2);

			struct sockaddr_in serv_addr;
			socklen_t serv_size = sizeof(serv_addr);
			bzero(&serv_addr, serv_size);

			serv_addr.sin_family = AF_INET;
			serv_addr.sin_port = htons(PORT);
			serv_addr.sin_addr.s_addr = inet_addr(players[2].ip);

			int connexion = connect(players[1].sock, (struct sockaddr *) &serv_addr, serv_size);
			int connexion2 = connect(players[2].sock, (struct sockaddr *) &serv_addr, serv_size);
			if (connexion == ERROR) {
				close(fd_py_to_c[TUBE_LECT]);
				close(fd_c_to_py[TUBE_ECRI]);
				close_serv();
				error("Erreur de connection!");
			}
			if (connexion2 == ERROR) {
				close(fd_py_to_c[TUBE_LECT]);
				close(fd_c_to_py[TUBE_ECRI]);
				close_serv();
				error("Erreur de connection!");
			}
			printf("Connecté aux autres joueurs !");

			char buff[PACKET_SIZE + 1];
			recuperer_packet(buff, players[1].sock);
			sscanf(buff, "PSEUDO %s", players[1].pseudo);
			sprintf(buff, "PSEUDO %s", pseudo);
			send_packet(buff, players[1].sock);
			printf("Pseudo du joueur 1: %s\n", players[1].pseudo);
			sprintf(buff, "NEW %s", players[1].pseudo);
			send_packet(buff, fd_c_to_py[TUBE_ECRI]);

			recuperer_packet(buff, players[2].sock);
			sscanf(buff, "PSEUDO %s", players[2].pseudo);
			sprintf(buff, "PSEUDO %s", pseudo);
			send_packet(buff, players[2].sock);
			printf("Pseudo du joueur 2: %s\n", players[2].pseudo);
			sprintf(buff, "NEW %s", players[2].pseudo);
			send_packet(buff, fd_c_to_py[TUBE_ECRI]);
		}
	}
}

void handle_new_connection() {
	struct sockaddr_in client_addr;
	socklen_t client_size = sizeof(client_addr);
	bzero(&client_addr, client_size);

	int cli_sock = accept(serv_sock, (struct sockaddr *) &client_addr, &client_size);
	if (cli_sock == ERROR) {
		close(fd_py_to_c[TUBE_LECT]);
		close(fd_c_to_py[TUBE_ECRI]);
		close_serv();
		error("Erreur de accept!");
	}

	printf("Nouveau joueur accepté, sock : %d\n", cli_sock);

	int added = FALSE;
	int indice = ERROR;

	if (nb_cli != MAX_CLI) {
		for (int i = 0; i < MAX_CLI; i++) {
			if (players[i].sock == ERROR) {
				players[i].sock = cli_sock;
				strcpy(players[i].ip, inet_ntoa(((struct sockaddr_in) client_addr).sin_addr));
				players[i].port = PORT;
				char buff[PACKET_SIZE + 1];
				sprintf(buff, "PSEUDO %s", pseudo);
				send_packet(buff, players[i].sock);
				recuperer_packet(buff, players[i].sock);
				added += sscanf(buff, "PSEUDO %s", players[i].pseudo);
				if (!added) { // erreur de communication = reset et refus du joueur
					players[i].port = ERROR;
					players[i].sock = ERROR;
					players[i].ip[0] = '\0';
					players[i].pseudo[0] = '\0';
				}
				else indice = i; // on recupere l'indice d'ajout
				break;
			}
		}
	}

	if (!added) {
		close(cli_sock);
		fprintf(stderr, "Impossible d'ajouter le nouveaux joueur, la partie est pleine!\n");
	}
	else {
		nb_cli++;
		char buff[PACKET_SIZE + 1];
		buff[0] = '\0';
		if (am_i_host) { // createur de la partie
			if (nb_cli > 1) {
				for (int i = 0; i < MAX_CLI; i++) {
					if (i != indice && players[i].sock != ERROR) {
						strcat(buff, players[i].ip);
						strcat(buff, " ");
					}
				}
			}
			else strcpy(buff, "FIRST");
			send_packet(buff, cli_sock);
		}
		else {
			strcpy(buff, "FIRST");
			send_packet(buff, cli_sock);
		}
		sprintf(buff, "NEW %s", players[indice].pseudo);
		send_packet(buff, fd_c_to_py[TUBE_ECRI]);
	}
}

void recuperer_packet(char buff[PACKET_SIZE + 1], int fd) {
	retour = read(fd, buff, PACKET_SIZE);
	if (retour == ERROR) {
		close(fd_py_to_c[TUBE_ECRI]);
		close(fd_c_to_py[TUBE_LECT]);
		if (is_serv_launched) close_serv();
		error("Erreur de lecture");
	}

	else buff[retour] = '\0';
}

void send_packet(char buff[PACKET_SIZE + 1], int fd) {
	int retour = write(fd, buff, strlen(buff));
	if (retour == ERROR) {
		close(fd_py_to_c[TUBE_ECRI]);
		close(fd_c_to_py[TUBE_LECT]);
		if (is_serv_launched) close_serv();
		error("Erreur d'ecriture");
	}
}

fd_set create_set(int *max_fd) {
	fd_set set;
	FD_ZERO(&set);
	FD_SET(fd_py_to_c[TUBE_LECT], &set); // on met le tube dans lequel on lit les messages du python
	*max_fd = fd_py_to_c[TUBE_LECT];

	if (is_serv_launched) {
		FD_SET(serv_sock, &set); // on met le socket serveur sur lequel on attend les messages des autres joueurs
		if (*max_fd < serv_sock) *max_fd = serv_sock; // on fait en sorte que *max_fd valle toujours la valeur du plus grand

		for (int i = 0; i < MAX_CLI; i++) {
			if (players[i].sock != ERROR) {
				FD_SET(players[i].sock, &set);
				if (*max_fd < players[i].sock) *max_fd = players[i].sock;
			}
		}
	}

	return set;
}

void create_serv() {
	serv_sock = socket(AF_INET, SOCK_STREAM, 0);
	if (serv_sock == ERROR) {
		close(fd_py_to_c[TUBE_LECT]);
		close(fd_c_to_py[TUBE_ECRI]);
		error("Erreur de création de la socket!");
	}

	int val = TRUE;
	retour = setsockopt(serv_sock, SOL_SOCKET, SO_REUSEADDR, &val, sizeof(val));
	if (retour == ERROR) {
		close(fd_py_to_c[TUBE_LECT]);
		close(fd_c_to_py[TUBE_ECRI]);
		close(serv_sock);
		error("Erreur de setsockopt!");
	}

	val = TRUE;
	retour = setsockopt(serv_sock, SOL_SOCKET, SO_REUSEPORT, &val, sizeof(val));
	if (retour == ERROR) {
		close(fd_py_to_c[TUBE_LECT]);
		close(fd_c_to_py[TUBE_ECRI]);
		close(serv_sock);
		error("Erreur de setsockopt!");
	}

	struct sockaddr_in serv_addr;
	socklen_t serv_size = sizeof(serv_addr);
	bzero(&serv_addr, serv_size);

	serv_addr.sin_family = AF_INET;
	serv_addr.sin_port = htons(PORT);
	serv_addr.sin_addr.s_addr = htonl(INADDR_ANY);

	retour = bind(serv_sock, (struct sockaddr *) &serv_addr, serv_size);
	if (retour == ERROR) {
		close(fd_py_to_c[TUBE_LECT]);
		close(fd_c_to_py[TUBE_ECRI]);
		if (is_serv_launched) close_serv();
		error("Erreur de bind de la socket!");
	}

	retour = listen(serv_sock, MAX_CLI);
	if (retour == ERROR) {
		close(fd_py_to_c[TUBE_LECT]);
		close(fd_c_to_py[TUBE_ECRI]);
		if (is_serv_launched) close_serv();
		error("Erreur de listen de la socket!");
	}

	is_serv_launched = TRUE;
	printf("Serveur lancé, en attente de connexion...\n");
}

void launch_python() {
	// fermer les parties de tubes inutiles
	close(fd_py_to_c[TUBE_LECT]);
	close(fd_c_to_py[TUBE_ECRI]);

	// passer la lecture en non bloquant
	fcntl(fd_c_to_py[TUBE_LECT], F_SETFL, O_NONBLOCK);

	// préparation des arguments
	char *cmd = "python3.10";
	char *launchfile = "main.py";

	int len = nbdigit(fd_py_to_c[TUBE_ECRI]);
	char arg1[len + 1];
	sprintf(arg1, "%d", fd_py_to_c[TUBE_ECRI]);

	len = nbdigit(fd_c_to_py[TUBE_LECT]);
	char arg2[len + 1];
	sprintf(arg2, "%d", fd_c_to_py[TUBE_LECT]);

	// création du tableau d'arguments
	char *tab[5] = { cmd, launchfile, arg1, arg2, NULL };

	// lancement du programme python
	execvp(cmd, tab);

	// on arrive ici seulement en cas d'erreur du execvp
	close(fd_py_to_c[TUBE_ECRI]);
	close(fd_c_to_py[TUBE_LECT]);
	fprintf(stderr, "Erreur de lancement du programme python\n");
	exit(EXIT_FAILURE);
}

void creer_tubes() {
	retour = pipe(fd_py_to_c);
	if (retour == ERROR) error("Erreur lors de la création du tube");

	retour = pipe(fd_c_to_py);
	if (retour == ERROR) {
		close_tube(fd_py_to_c);
		error("Erreur lors de la création du tube");
	}
}

int nbdigit(int n) {
	int res = 1;
	while (n > 9) {
		res++;
		n /= 10;
	}
	return res;
}

void error(char *mess) {
	perror(mess);
	exit(EXIT_FAILURE);
}

void close_tube(int tube[TUBE_SIZE]) {
	close(tube[TUBE_ECRI]);
	close(tube[TUBE_LECT]);
}

void close_serv() {
	for (int i = 0; i < MAX_CLI; i++) {
		if (players[i].sock != ERROR) {
			close(players[i].sock);
			players[i].sock = ERROR;
			players[i].ip[0] = '\0';
			players[i].pseudo[0] = '\0';
			players[i].port = ERROR;
		}
	}

	close(serv_sock);
	serv_sock = ERROR;
	is_serv_launched = FALSE;
}
