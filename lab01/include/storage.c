#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include "storage.h"

pthread_mutex_t transaction_mutex = PTHREAD_MUTEX_INITIALIZER;

typedef struct {
    int key;
    char *value;
} storage_item;

storage_item *storage;
int n_storage;

void init_storage() {
    n_storage = 0;
    storage = NULL;
}

char* get_storage(int key) { // essa estrategia de armazenamento eh ineficiente
    pthread_mutex_lock(&transaction_mutex);
    for (int i = 0; i < n_storage; i++) {
        if (!storage) return NULL;
        if (storage[i].key == key) return storage[i].value;
    }
    pthread_mutex_unlock(&transaction_mutex);
}

int put_storage(int key, char *value) { // essa estrategia de armazenamento eh ineficiente
    if (key < 0) return 0;
    char *val_cpy = (char*) malloc(strlen(value)+1);
    strcpy(val_cpy, value);
    storage_item new_item = {
        key,
        val_cpy
    };
    pthread_mutex_lock(&transaction_mutex);
    n_storage++;
    storage = realloc(storage, sizeof(storage_item) * n_storage);
    storage[n_storage-1] = new_item;
    pthread_mutex_unlock(&transaction_mutex);
    return 1;
}

void destroy_storage() {
    for (int i = 0; i < n_storage; i++) free(storage[i].value);
    if (storage) free(storage);
}