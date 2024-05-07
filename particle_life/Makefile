CC=gcc
CFLAGS=-O2 -Wall -pedantic -std=c89
LFLAGS=-lSDL2 -lm

SRCDIR=src
OBJDIR=obj
TESTDIR=tests

EXENAME=particle_life

all:	$(EXENAME)

clean:
	rm -f *.o \
	rm -f $(EXENAME)

run:	all
	./$(EXENAME)

$(EXENAME):	particle_life.o
	gcc -o $@ $^ $(LFLAGS)

particle_life.o:	particle_life.c
	$(CC) $(CFLAGS) -c -o $@ $<
