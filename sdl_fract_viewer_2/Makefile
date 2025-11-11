CC=gcc
CFLAGS=-O9 -Wall -Werror -pedantic -std=c89
LFLAGS=-lSDL2 -lm

SRCDIR=src
OBJDIR=obj
TESTDIR=tests

EXENAME=fv

.PHONY: all clean run

all:	$(EXENAME)

clean:
	rm -f $(OBJDIR)/*.o
	rm -f $(TESTDIR)/*
	rm -f $(EXENAME)

run:	all
	./$(EXENAME)

$(EXENAME):	$(OBJDIR)/main.o $(OBJDIR)/gfx.o
	gcc -o $@ $^ $(LFLAGS)

$(OBJDIR)/main.o:	$(SRCDIR)/main.c
	@mkdir -p $(OBJDIR)
	$(CC) $(CFLAGS) -c -o $@ $<

$(OBJDIR)/gfx.o:	$(SRCDIR)/gfx.c $(SRCDIR)/gfx.h
	@mkdir -p $(OBJDIR)
	$(CC) $(CFLAGS) -c -o $@ $<
