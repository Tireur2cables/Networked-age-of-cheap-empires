#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <stdlib.h>

void error(char *);

int main(int argc, char const *argv[]) {
	int pid = fork();
	switch (pid) {
		case -1 : error("Erreur lors du fork");
		case 0 : {
			char *cmd = "python3";
			char *launchfile = "main.py";
			char *tab[3] = { cmd, launchfile, NULL };
			execvp(cmd, tab);
		}
		default : printf("Je suis le père (programme C en attente)\n");
	}

	return 0;
}

void error(char *mess) {
	perror(mess);
	exit(EXIT_FAILURE);
}
