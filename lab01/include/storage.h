#ifndef STORAGE_H
#define STORAGE_H

void init_storage();

char* get_storage(int key);

int put_storage(int key, char *value);

void destroy_storage();

#endif