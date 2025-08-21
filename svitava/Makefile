.PHONY: all clean

CC=gcc
CFLAGS=-Wall -pedantic -ansi
LFLAGS=-lm

all: svitava.so

clean:
	rm -f svitava.so
	rm -f *.bmp
	rm -f *.ppm
	rm -f *.tga

svitava.so:	svitava.c
	$(CC) $(CFLAGS) $(LFLAGS) -shared -Wl,-soname,svitava -o $@ -fPIC $<
