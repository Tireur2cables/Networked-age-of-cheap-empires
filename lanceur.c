#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <stdlib.h>
#include <string.h>

#define ERROR -1

int nbdigit(int);
void error(char *);

int main(int argc, char const *argv[]) {

	int fd_py_to_c[2];
	int retour = pipe(fd_py_to_c);
	if (retour == ERROR) error("Erreur lors de la création du tube");

	int fd_c_to_py[2];
	retour = pipe(fd_c_to_py);
	if (retour == ERROR) error("Erreur lors de la création du tube");
	// fd[0] // lecture
	// fd[1] // ecriture
	int pid = fork();
	switch (pid) {
		case ERROR : error("Erreur lors du fork");
		case 0 : {
			close(fd_py_to_c[0]);
			close(fd_c_to_py[1]);

			char *cmd = "python3";
			char *launchfile = "main.py";

			int len = nbdigit(fd_py_to_c[1]);
			char arg1[len + 1];
			sprintf(arg1, "%d", fd_py_to_c[1]);

			len = nbdigit(fd_c_to_py[0]);
			char arg2[len + 1];
			sprintf(arg2, "%d", fd_c_to_py[0]);

			char *tab[5] = { cmd, launchfile, arg1, arg2, NULL };
			execvp(cmd, tab);
		}
		default : {
			close(fd_py_to_c[1]);
			close(fd_c_to_py[0]);
			printf("Je suis le père (programme C en attente)\n");

			char buff[512];
			retour = read(fd_py_to_c[0], buff, 511);
			if (retour == ERROR) error("Erreur de lecture dans le tube");
			buff[retour] = '\0';

			if (strcmp(buff, "STOP") == 0) {
				printf("Je me stoppe\n");
				close(fd_py_to_c[0]);
				close(fd_c_to_py[1]);
				exit(EXIT_SUCCESS);
			}
			else {
				printf("buff non reconnu : %s\n", buff);
			}

		}
	}

	return 0;
}

int nbdigit(int n) {
	int res = 1;
	while (n>9) {
		res++;
		n/=10;
	}
	return res;
}


void error(char *mess) {
	perror(mess);
	exit(EXIT_FAILURE);
}
