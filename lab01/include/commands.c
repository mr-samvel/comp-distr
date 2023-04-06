#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "commands.h"
#include "common.h"
#include "storage.h"

#define DOCS_LISTCMDS "listcmds -> Retorna o no. de comandos e suas chamadas."
#define LISTCMDS "listcmds"

#define DOCS_DOCS "docs -> Retorna a descricao de uso dos comandos e seus retornos."
#define DOCS "docs"

#define DOCS_QUIT "quit -> Encerra a conexão com o servidor."
#define QUIT "quit"

#define DOCS_GET "get intkey -> Retorna o valor armazenado na chave intkey. Ex: get 2"
#define GET "get"

#define DOCS_PUT "put intkey strvalue -> Retorna o valor armazenado na chave intkey. Ex: put 2 string que sera armazenada"
#define PUT "put"

char *DOCS_AVAILABLE_COMMANDS[] = {
    DOCS_LISTCMDS,
    DOCS_DOCS,
    DOCS_QUIT,
    DOCS_GET,
    DOCS_PUT
};

char *AVAILABLE_COMMANDS[] = {
    LISTCMDS,
    DOCS,
    QUIT,
    GET,
    PUT
};
const int N_AVAILABLE_COMMANDS = sizeof(AVAILABLE_COMMANDS) / sizeof(char*);

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
    for (int i = 0; i < N_AVAILABLE_COMMANDS; i++) {
        response_size += strlen(AVAILABLE_COMMANDS[i]) + 2;
    }
    char *response = (char*) malloc(sizeof(char) * response_size);
    sprintf(response, "%d", N_AVAILABLE_COMMANDS);
    strcat(response, " ");
    strcat(response, expand(AVAILABLE_COMMANDS, " ", N_AVAILABLE_COMMANDS));
    return response;
}

char* docs() {
    char *response = (char*) malloc(sizeof(char));
    response[0] = '\0';
    for (int i = 0; i < N_AVAILABLE_COMMANDS; i++) {
        response = (char*) realloc(response, sizeof(char) * (strlen(response) + strlen(DOCS_AVAILABLE_COMMANDS[i])) + 2);
        strcat(response, "\n");
        strcat(response, DOCS_AVAILABLE_COMMANDS[i]);
        strcat(response, "\n");
    }
    return response;
}

char* quit() {
    return NULL;
}

char* get(char *key) {
    int k = atoi(key);
    char *response = get_storage(k);
    if (!response) response = "(null)";
    return response;
}

char* put(char *key, char *value) {
    int k = atoi(key);
    char *response;
    if (put_storage(k, value)) response = "Item adicionado com sucesso.\n";
    else response = "Erro ao adicionar item!\n";
    return response;
}