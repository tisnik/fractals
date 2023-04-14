CC=gcc
CFLAGS=-ffast-math -O2 -Wall -pedantic -std=c89
LFLAGS=-lSDL2 -lm

SRCDIR=src
OBJDIR=obj

EXENAME=ifs_anim

all:	$(EXENAME)

clean:
	rm -f $(OBJDIR)/* \
	rm -f $(EXENAME)

$(EXENAME):	$(OBJDIR)/ifs_anim.o
	gcc -o $(EXENAME) $? $(LFLAGS)

$(OBJDIR)/ifs_anim.o:	$(SRCDIR)/ifs_anim.c
	$(CC) $(CFLAGS) -c -o $@ $<

