IDIR=./include
_DEPS=common.c commands.c storage.c
DEPS=$(patsubst %,$(IDIR)/%,$(_DEPS))

CFLAGS=-I $(IDIR) -ggdb
LIBS=-pthread

SRC=src
OUT=bin

server:
	gcc $(LIBS) $(SRC)/server.c $(DEPS) -o $(OUT)/server $(CFLAGS)

client: 
	gcc $(LIBS) $(SRC)/client.c $(DEPS) -o $(OUT)/client $(CFLAGS)

all: clean server client

clean:
	rm -rf bin/*