#ifndef COMMANDS_H
#define COMMANDS_H

char* commands(char *request);

char* listcmds();

char* docs();

char* quit();

char* get(char *key);

char* put(char *key, char *value);

#endif