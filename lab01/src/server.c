#include <sys/types.h>
#include <sys/socket.h>
#include <stdio.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <stdlib.h>
#include <pthread.h>
#include <semaphore.h>
#include <string.h>
#include "common.h"
#include "commands.h"

#define MAX_CLIENTS 10
#define BUFFER_SIZE 512
#define SERVER_PORT 9734

int active_sockets[MAX_CLIENTS];
int n_active_sockets = 0;
pthread_t sockets_thread_pool[MAX_CLIENTS];
pthread_mutex_t mutex_active_sockets = PTHREAD_MUTEX_INITIALIZER;

typedef struct {
  int server_sockfd;
  void *(*f_handle_socket_connection)(void *);
} listen_socket_arg;

void show_banner() {
  printf("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n");
  printf("! Lab01 - Implementação de um serviço Chave-Valor Distribuído   !\n");
  printf("! Este é o servidor. Aqui você receberá comandos dos clientes.  !\n");
  printf("! Digite quit para encerrar.                                    !\n");
  printf("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n");
}

int start_server() {
  int server_sockfd = socket(AF_INET, SOCK_STREAM, 0);
  struct sockaddr_in server_address;
  server_address.sin_family = AF_INET;
  //server_address.sin_addr.s_addr = inet_addr("127.0.0.1");
  //server_address.sin_addr.s_addr = inet_addr("192.168.0.15");
  server_address.sin_addr.s_addr = htonl(INADDR_ANY);
  server_address.sin_port = htons(SERVER_PORT);
  bind(server_sockfd, (struct sockaddr *)&server_address, sizeof(server_address));
	listen(server_sockfd, 5);
  printf("Servidor iniciou na porta %d.\n", SERVER_PORT);
  return server_sockfd;
}

int accept_new_socket(int server_sockfd) {
  struct sockaddr_in client_address;
  int client_len = sizeof(client_address);
  int client_sockfd = accept(server_sockfd,(struct sockaddr *)&client_address, &client_len);
  pthread_mutex_lock(&mutex_active_sockets);
  active_sockets[n_active_sockets] = client_sockfd;
  n_active_sockets++;
  pthread_mutex_unlock(&mutex_active_sockets);
  printf("\nNova conexão no socket %d.\n", client_sockfd);
  printf("Conexões ativas: %d.\n", n_active_sockets);
  return client_sockfd;
}

void disconnect_socket(int sockfd) {
  pthread_mutex_lock(&mutex_active_sockets);
  n_active_sockets--;
  pthread_mutex_unlock(&mutex_active_sockets);
  printf("\nConexão no socket %d desfeita.\n", sockfd);
  printf("Conexões ativas: %d.\n", n_active_sockets);
  close(sockfd);
}

void *listen_socket(void *arg) {
  listen_socket_arg args = *(listen_socket_arg *) arg;
  int server_sockfd = args.server_sockfd;
  int client_sockfd;
  while(1) {
    if (n_active_sockets < MAX_CLIENTS) {
      client_sockfd = accept_new_socket(server_sockfd);
      pthread_create(&sockets_thread_pool[n_active_sockets-1], NULL, args.f_handle_socket_connection, (void *) &client_sockfd);
    } else {
      printf("\nNúmero máximo de conexões alcançado.\n");
      printf("Conexões ativas: %d.\n", n_active_sockets);
    }
	}
}

void *handle_socket_connection(void *arg) {
  int client_sockfd = *(int *) arg;
  char buffer[BUFFER_SIZE];
  size_t bytes_received;
  while((bytes_received = read(client_sockfd, buffer, BUFFER_SIZE)) > 0) {
    printf("\nMensagem recebida de cliente no socket %d: %s\n", client_sockfd, buffer);
    char *response = commands(buffer);
    printf("\n RESPONSE : %s\n", response);
    if (response == NULL) break;
    write(client_sockfd, response, sizeof(response));
  }
  disconnect_socket(client_sockfd);
}

void handle_ui() {
  int input_max = 124, max_words = 2;
  while (1) {
    char **input = read_from_ui(input_max, max_words); // blocking
    if (str_in_array("quit", input, max_words)) {
      break;
    }
  }
}

int main() {
  show_banner();
  
  int server_sockfd = start_server();
  pthread_t socket_listener_thread;
  listen_socket_arg socket_listener_args = {
    server_sockfd,
    &handle_socket_connection
  };
  pthread_create(&socket_listener_thread, NULL, listen_socket, (void *) &socket_listener_args);
    
  handle_ui();

  for (int i = 0; i < n_active_sockets; i++) {
    disconnect_socket(active_sockets[i]);
    pthread_cancel(sockets_thread_pool[i]);
  }
  return shutdown(server_sockfd, SHUT_RDWR);
}
