#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <stdlib.h>
#include <string.h>
#include <sys/select.h>

#define ERROR -1
#define TUBE_SIZE 2
#define TUBE_LECT 0
#define TUBE_ECRI 1
#define PACKET_SIZE 512 // a determiner

int nbdigit(int);
void error(char *);
void creer_tube(int [TUBE_SIZE]);
void launch_communication();
void launch_python();
fd_set create_set(int *);
void recuperer_packet(char [PACKET_SIZE + 1], int);

int fd_py_to_c[TUBE_SIZE];
int fd_c_to_py[TUBE_SIZE];

int main(int argc, char const *argv[]) {
	// initialisation des tubes
	creer_tube(fd_py_to_c);
	creer_tube(fd_c_to_py);

	int pid = fork();
	switch (pid) {
		case ERROR : error("Erreur lors du fork");
		case 0 : launch_python();
		default : launch_communication();
	}

	return 0;
}

void launch_communication() {
	// on ferme les parties des tubes que l'on utilisera pas
	close(fd_py_to_c[TUBE_ECRI]);
	close(fd_c_to_py[TUBE_LECT]);

	printf("Je suis le père (programme C en attente)\n");

	// on créer l'ensembles de file descriptor sur lesquels on attends des messages
	int max_fd;
	fd_set set = create_set(&max_fd);

	int retour = select(max_fd + 1, &set, NULL, NULL, NULL);
	if (retour == ERROR) error("Erreur du select");

	char buff[PACKET_SIZE + 1];
	// on regarde qui veut nous envoyer un message (python ou sockets)
	if (FD_ISSET(fd_py_to_c[TUBE_LECT], &set)) // le programme python veut envoyer un message
		recuperer_packet(buff, fd_py_to_c[TUBE_LECT]);

	// if (FD_ISSET(sock, &set)) // on fera pareil avec les sockets

	if (strcmp(buff, "STOP") == 0) {
		printf("Je me stoppe\n");
		close(fd_py_to_c[TUBE_LECT]);
		close(fd_c_to_py[TUBE_ECRI]);
		exit(EXIT_SUCCESS);
	}
	else {
		printf("message non reconnu : %s\n", buff);
	}

}

void recuperer_packet(char buff[PACKET_SIZE + 1], int fd) {
	int retour = read(fd, buff, PACKET_SIZE);
	if (retour == ERROR) error("Erreur de lecture");
	buff[retour] = '\0';
}

fd_set create_set(int *max_fd) {
	fd_set set;
	FD_ZERO(&set);
	FD_SET(fd_py_to_c[TUBE_LECT], &set); // on met le tube dans lequel on lit les message du python
	*max_fd = fd_py_to_c[TUBE_LECT];

	// FD_SET(sock, &set); // on met les sockets sur lesquels on attend les messages des autres
	// if (*max_fd < sock) *max_fd = sock; // on fait en sorte que *max_fd valle toujours la valeur du plus grand

	return set;
}

void creer_tube(int fd_tube[TUBE_SIZE]) {
	int retour = pipe(fd_tube);
	if (retour == ERROR) error("Erreur lors de la création du tube");
}

void launch_python() {
	// fermer les parties de tubes inutiles
	close(fd_py_to_c[TUBE_LECT]);
	close(fd_c_to_py[TUBE_ECRI]);

	// préparation des arguments
	char *cmd = "python3";
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
