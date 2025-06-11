.PHONY: all clean

CC=gcc
CFLAGS=-Wall -pedantic -ansi
LFLAGS=-lm

all: svitava.so

clean:
	rm -f svitava.so

svitava.so:	svitava.c
	$(CC) $(CFLAGS) $(LFLAGS) -shared -Wl,-soname,svitava -o $@ -fPIC $<
