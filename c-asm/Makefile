CC = gcc
CFLAGS = -Wall -Wextra -g

all: clean 12-fact glob-loc-arg code_translated

12-fact: base.o 12-fact.o
	$(CC) $(CFLAGS) -o $@ $^

glob-loc-arg: base.o glob-loc-arg.o
	$(CC) $(CFLAGS) -o $@ $^

code_translated: base.o code_translated.o
	$(CC) $(CFLAGS) -o $@ $^

%.o: %.c
	$(CC) $(CFLAGS) -c $<

code_translated.o: hacks.h base.h
base.o: hacks.h base.h
12-fact.o: hacks.h base.h
glob-loc-arg.o: hacks.h base.h

clean: 
	rm -f *.o 
	rm -f 12-fact
	rm -f glob-loc-arg
	rm -f code_translated

.PHONY: all
