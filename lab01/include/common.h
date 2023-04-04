#ifndef COMMON_H
#define COMMON_H

char** split(char *string, const char *delimiter, int max_array_size);

char* expand(char **str_arr, const char *expander, int arr_size);

int str_in_array(char *str, char **arr, int arr_size);

char** read_from_ui(const int INPUT_MAX, const int MAX_WORDS);

#endif