from socket import socket, SOL_SOCKET, SO_REUSEADDR
import select
from typing import Callable, Dict, List
from threading import Thread

class ConnectionHandler:
    def __init__(self, node_id: int, addresses: Dict[int, str], on_read_callback: Callable) -> None:
        self.__addresses_map = addresses
        self.__node_id = node_id
        self.__on_read_cb = on_read_callback

        # server socket
        self.__server_socket: socket = socket()
        self.__server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # allow reuse
        self.__server_socket.bind(addresses[node_id])
        self.__server_socket.listen(5)

        self.__read_sockets: List[socket] = []  # list
        self.__write_sockets: Dict[int, socket] = {}  # dict from node_id to socket

        self.__trailing_msg = ""

    @property
    def __all_read_sockets(self):
        return list(self.__read_sockets) + [self.__server_socket]

    def __run(self):
        while True:
            try:
                ready_to_read, _, __ = select.select(self.__all_read_sockets, [], [])
            except ValueError:
                for i, sock in enumerate(self.__read_sockets):
                    if sock.fileno() == -1:  # closed
                        self.__read_sockets.pop(i)
                continue

            for sock in ready_to_read:
                if sock == self.__server_socket:
                    cs, _ = self.__server_socket.accept()
                    self.__read_sockets.append(cs)
                else:
                    try:
                        self.receive_messages_from_socket(sock)
                    except Exception as e:
                        raise Exception("Erro inesperado ", e)

    def __connect_to_node(self, node_id):
        cs = socket()
        cs.connect(self.__addresses_map[node_id])
        self.__write_sockets[node_id] = cs

    def run(self):
        t = Thread(target=self.__run)
        t.daemon = False
        t.start()

    def send_message_to_node(self, node_id, msg: str):
        msg += "\n"
        existing_sock = self.__write_sockets.get(node_id)
        if not existing_sock:
            try:
                self.__connect_to_node(node_id)
            except ConnectionRefusedError:
                raise Exception(f"Nodo-{node_id} não aceitou conexão")

        self.__write_sockets[node_id].send(msg.encode())

    def receive_messages_from_socket(self, sock: socket, buff_size: int = 1024):
        msgs = sock.recv(buff_size).decode()
        if not msgs:
            sock.close()
        else:
            *list_of_msgs, temp = msgs.split("\n")
            list_of_msgs[0] = self.__trailing_msg + list_of_msgs[0]
            self.__trailing_msg = temp
            for msg in list_of_msgs:
                self.__on_read_cb(msg)

    def close(self):
        self.__server_socket.close()
        for write_sock in self.__write_sockets.values():
            write_sock.close()
        for read_sock in self.__read_sockets:
            read_sock.close()
