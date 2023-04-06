#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "commands.h"
#include "common.h"

#define LISTCMDS "listcmds"
#define DOCS "docs"
#define QUIT "quit"
#define GET "get"
#define PUT "put"

char *available_commands[] = {
    LISTCMDS,
    DOCS,
    QUIT,
    GET,
    PUT
};
int n_available_commands = sizeof(available_commands) / sizeof(char*);

char* commands(char *request) {
    char **splitted_req = split(request, " ", 3);
    char *response;
    if (strcmp(splitted_req[0], LISTCMDS) == 0) response = listcmds();
    else if (strcmp(splitted_req[0], DOCS) == 0) response = docs();
    else if (strcmp(splitted_req[0], QUIT) == 0) response = quit();
    else if (strcmp(splitted_req[0], GET) == 0) response = get(splitted_req[1]);
    else if (strcmp(splitted_req[0], PUT) == 0) response = put(splitted_req[1], splitted_req[2]);
    else response = "Comando incompreensível.";
    return response;
}

char* listcmds() {
    int response_size = 0;
    for (int i = 0; i < n_available_commands; i++) {
        response_size += strlen(available_commands[i]) + 2;
    }
    char *response = (char*) malloc(sizeof(char) * response_size);
    sprintf(response, "%d", n_available_commands);
    strcat(response, " ");
    strcat(response, expand(available_commands, " ", n_available_commands));
    return response;
}

char* docs() {
    return NULL;
}

char* quit() {
    return NULL;
}

char* get(char *key) {
    return NULL;
}

char* put(char *key, char *value) {
    return NULL;
}