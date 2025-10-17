.PHONY: all clean

CC=gcc
CFLAGS=-Wall -pedantic -ansi
LFLAGS=-lm

SDL_LFLAGS=-lSDL2

all: svitava.so

clean:
	rm -f svitava
	rm -f svitava.so
	rm -f *.bmp
	rm -f *.ppm
	rm -f *.tga
	rm -f *.o

svitava.so:	svitava.c
	$(CC) $(CFLAGS) $(LFLAGS) -shared -Wl,-soname,svitava -o $@ -fPIC $<

svitava:	ui.o svitava.o
	gcc -o $@ $^ $(SDL_LFLAGS) $(LFLAGS)

ui.o:	ui.c
	$(CC) $(CFLAGS) -c -o $@ $<

svitava.o:	svitava_.c
	$(CC) $(CFLAGS) -c -o $@ $< -DNO_MAIN
