IDIR=./include
_DEPS=common.c commands.c
DEPS=$(patsubst %,$(IDIR)/%,$(_DEPS))

CFLAGS=-I $(IDIR)
LIBS=-pthread

SRC=src
OUT=bin

# gcc main_server.c common.c -o main_server -pthread

server: 
	gcc $(LIBS) $(SRC)/server.c $(DEPS) -o $(OUT)/server $(CFLAGS)

client: 
	gcc $(LIBS) $(SRC)/client.c $(DEPS) -o $(OUT)/client $(CFLAGS)

clean:
	rm -rf bin/*