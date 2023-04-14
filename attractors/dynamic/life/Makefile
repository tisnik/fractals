CC=gcc
CFLAGS=-O2 -Wall -pedantic -std=c89
LFLAGS=-lSDL2 -lm

SRCDIR=src
OBJDIR=obj
TESTDIR=tests

EXENAME=life

all:	$(EXENAME)

clean:
	rm -f $(OBJDIR)/* \
	rm -f $(TESTDIR)/* \
	rm -f $(EXENAME)

run:	all
	./$(EXENAME)

$(EXENAME):	$(OBJDIR)/main.o $(OBJDIR)/gfx.o
	gcc -o $@ $^ $(LFLAGS)

$(OBJDIR)/main.o:	$(SRCDIR)/main.c
	$(CC) $(CFLAGS) -c -o $@ $<

$(OBJDIR)/gfx.o:	$(SRCDIR)/gfx.c
	$(CC) $(CFLAGS) -c -o $@ $<
