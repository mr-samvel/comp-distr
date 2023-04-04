#include "common.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char** split(char *string, const char *delimiter, int max_array_size) {
  char **words = (char**) malloc(sizeof(char*) * max_array_size);
  char *token = strtok(string, delimiter);
  int i = 0;
  while (token != NULL) {
    if (i < max_array_size) {
      words[i]= (char*) malloc(sizeof(char) * (strlen(token) + 1));
      strcpy(words[i], token);
      i++;
    } else {
      int j = max_array_size-1;
      int remaining = strlen(token);
      words[j] = (char*) realloc(words[j], sizeof(words[j]) + (sizeof(char) * strlen(token) + 1));
      strcat(words[j], delimiter);
      strcat(words[j], token);
    }
    token = strtok(NULL, delimiter); // prossegue para prox token
  }
  return words;
}

char* expand(char **str_arr, const char *expander, int arr_size) {
  char *expanded = (char*) malloc(sizeof(str_arr[0])+1);
  strcpy(expanded, str_arr[0]);
  for (int i = 1; i < arr_size; i++) {
    expanded = (char*) realloc(expanded, sizeof(expanded) + sizeof(str_arr[i]) + 1);
    strcat(expanded, expander);
    strcat(expanded, str_arr[i]);
  }
  return expanded;
}

int str_in_array(char *str, char **arr, int arr_size) {
  for (int i = 0; i < arr_size; i++)
    if (strcmp(str, arr[i]) == 0) return 1;
  return 0;
}

char** read_from_ui(const int INPUT_MAX, const int MAX_WORDS) {
  char input[INPUT_MAX];
  fgets(input, INPUT_MAX, stdin);
  input[strcspn(input, "\n")] = 0; // remove \n
  char **words = split(input, " ", MAX_WORDS);
  return words;
}