.PHONY: all clean cleanall

CC = gcc
CFLAGS = -Wall -g
LDLIBS =
ALL = lanceur

all : $(ALL)
lanceur : lanceur.o

lanceur.o : lanceur.c

clean :
	rm -rf *~
cleanall : clean
	rm -rf $(ALL) *.o

