# Ping-Pong MQTT

Lab03 de INE5418 - Computação Distribuída
Dupla: Eduardo Borges Siqueira (19100523) e Samuel Moreira Ransolin (19102348)

## O que é

Escolhemos implementar um quase-jogo de ping-pong entre processos que se comunicam através de mensagens MQTT.
Existem 4 processos em `lab03/app/` que fazem com que isso aconteça:

- `ping` e `pong`: Jogam o ping-pong inscrevendo-se e postando suas jogadas no tópico 'ping-pong' de acordo com a última mensagem consumida dele. Podem sacar, rebater ou errar;
- `score`: Consome mensagens de 'ping-pong' e conforme `ping` ou `pong` erram, atualiza o placar postando no tópico 'placar';
- `ui`: Consome mensagens de 'ping-pong' e 'placar' e exibe de acordo no terminal.

## Instruções

Para facilitar o trabalho de configuração, containerizamos a aplicação, portanto basta ter instalado o Docker e Docker-compose.
Com esses requisitos atendidos, executar `docker-compose up` vai ser suficiente para levantar e configurar o broker e todos os processos para a execução do ping-pong.
