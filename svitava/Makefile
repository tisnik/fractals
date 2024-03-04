.PHONY: all clean

CC=gcc
CFLAGS=-Wall -pedantic -ansi

all: svitava.so

clean:
	rm -f svitava.so

svitava.so:	svitava.c
	$(CC) $(CFLAGS) -shared -Wl,-soname,svitava -o $@ -fPIC $<
