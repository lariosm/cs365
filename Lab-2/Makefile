DEBUG=y

CC=g++
CFLAGS= -Wall
LDFLAGS=

ifeq ($(DEBUG), 'y')
	CFLAGS += -DDEBUG -g
else
	CFLAGS += -O2
endif

.PHONY: all clean

all: bin/shell

bin/shell: obj/shell.o obj/parser.o obj/main.o
	$(CC) $^ -o $@

obj/%.o: src/%.cpp
	$(CC) -c $(CFLAGS) $< -o $@

clean:
	$(RM) *~ src/*~ src/#* obj/*.o bin/*
