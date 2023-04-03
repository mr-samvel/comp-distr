#include <sys/types.h>
#include <sys/socket.h>
#include <stdio.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>

#define INPUT_MAX 100
#define MAX_WORDS 3

void show_banner() {
  printf("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n");
  printf("! Lab01 - Implementação de um serviço Chave-Valor Distribuído   !\n");
  printf("! Este é o cliente. A partir deste terminal você poderá enviar  !\n");
  printf("! comandos ao servidor.                                         !\n");
  printf("! Invoque um comando chamando a função e passando os argumentos !\n");
  printf("! (quando houver) separados por espaço,                         !\n");
  printf("!    por exemplo: funcao arg1 arg2 arg3                         !\n");
  printf("! Digite quit para sair.                                        !\n");
  printf("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n");
}

char** split(char *string, const char *delimiter, size_t max_array_size) {
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

char* expand(char **str_arr, const char *expander, size_t arr_size) {
  char *expanded = (char*) malloc(sizeof(str_arr[0])+1);
  strcpy(expanded, str_arr[0]);
  for (int i = 1; i < arr_size; i++) {
    expanded = (char*) realloc(expanded, sizeof(expanded) + sizeof(str_arr[i]) + 1);
    strcat(expanded, expander);
    strcat(expanded, str_arr[i]);
  }
  return expanded;
}

int str_in_array(char *str, char **arr, size_t arr_size) {
  for (int i = 0; i < arr_size; i++)
    if (strcmp(str, arr[i]) == 0) return 1;
  return 0;
}

char** read_from_ui() {
  char input[INPUT_MAX];
  printf(">> ");
  fgets(input, INPUT_MAX, stdin);
  input[strcspn(input, "\n")] = 0; // remove \n
  char **words = split(input, " ", MAX_WORDS);
  return words;
}

int connect_to_server(const char *serv_addr, const int serv_port) {
  int sockfd = socket(AF_INET, SOCK_STREAM, 0);
  struct sockaddr_in addr;
  addr.sin_family = AF_INET;
  addr.sin_addr.s_addr = inet_addr(serv_addr);
  //address.sin_addr.s_addr = inet_addr("192.168.0.15");
  //address.sin_addr.s_addr = htonl(INADDR_ANY);
  addr.sin_port = htons(serv_port);

  if (connect(sockfd, (struct sockaddr *)&addr, sizeof(addr)) != -1)
    return sockfd;
  return -1;
}

char* post(int sockfd, char *cmd) {
  char *buffer = NULL;
  if (write(sockfd, cmd, sizeof(cmd)) != -1) {
    int status = 1;
    int len = 64, bytes_received = 0, cur_size = 0;
    while (status > 0) {
      if (bytes_received >= cur_size) {
        cur_size += len;
        char *tmp = realloc(buffer, cur_size);
        if (tmp == NULL) break;
        buffer = tmp;
      }
      status = read(sockfd, buffer+bytes_received, len);
      bytes_received += status;
    }
  } else {
    printf("Erro ao enviar comando ao servidor.\n");
  }
  return buffer;
}

char** get_available_commands(int sockfd) {
  char *listcmds_response = post(sockfd, "listcmds");
  int n_cmds = atoi(listcmds_response[0]);
  return split(listcmds_response, " ", n_cmds);
}

int main() {
  show_banner();

  const char *serv_addr = "127.0.0.1";
  const int serv_port = 9734;

  printf("Conectando ao servidor...\n");
  int sockfd = connect_to_server(serv_addr, serv_port);
  if(sockfd == -1) {
    perror("Conexão com o servidor falhou!");
    exit(1);
  }
  printf("Conectado!\n");

  char **available_cmds = get_available_commands(sockfd);
  int n_cmds = atoi(available_cmds[0]);
  available_cmds = available_cmds+1; // slice do primeiro elemento

  char **input;
  char *response;
  while (1) {
    input = read_from_ui();

    if (str_in_array(input[0], available_cmds, n_cmds)) {
      response = post(sockfd, expand(input, " ", MAX_WORDS));
      printf("Resposta: %s\n", response);
      if (strcmp(input[0], "quit") == 0) break;
    } else {
      printf("Comando incompreensível.\n");
    }
  }

  for (int i = 0; i < MAX_WORDS; i++) free(input[i]);
  free(input);
  close(sockfd);
	exit(0);
}
