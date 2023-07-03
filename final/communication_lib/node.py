from typing import Callable, Optional, List, Dict
from ._connection_handler import ConnectionHandler
from .utils.priority_queue import MessagePriorityQueue
from .utils.message import MessageType, Message
from threading import Lock

class NetworkNode:
    def __init__(self, id: int, addresses: Dict[int, str], on_deliver_callback: Callable):
        self.__id = id
        self.__all_nodes = list(addresses.keys())
        self.__on_deliver_cb = on_deliver_callback
        self.__conn_handler = ConnectionHandler(id, addresses, on_read_callback=self.receive)

        self.__clock = float(f"0.{id}")
        self.__clock_lock = Lock()

        self.__delivery_queue = MessagePriorityQueue()
        self.__conn_handler.run()

    @property
    def __other_nodes(self):
        return [node_id for node_id in self.__all_nodes if node_id != self.__id]

    def __update_clock(self, new_value: Optional[float] = None):
        with self.__clock_lock:
            self.__clock = max(int(self.__clock), int(new_value or 0)) + 1 + float(f"0.{self.__id}")
            return self.__clock
    
    def __send_to_nodes(self, message: str, nodes_ids: List[int]):
        new_clock = self.__update_clock()
        msg = Message(
            clock=new_clock,
            sender_id=self.__id,
            msg_type=MessageType.MESSAGE,
            msg_text=message,
        )
        self.__delivery_queue.push(msg)

        if len(nodes_ids) > 1:
            print(f"Nodo-{self.__id}: fazendo broadcast de mensagem com clock {new_clock}")
        else:
            print(f"Nodo-{self.__id}: enviando do nodo {self.__id} para {nodes_ids[0]} com clock {new_clock}")
        for node_id in nodes_ids:
            self.__conn_handler.send_message_to_node(node_id, str(msg))
       
    def __ack_and_deliver(self):
        while True:
            top = self.__delivery_queue.top
            if top:
                if self.__id not in top.acks:
                    msg = str(Message(clock=top.clock, sender_id=self.__id, msg_type=MessageType.ACK))
                    top.acks.append(self.__id)
                    for node_id in self.__other_nodes:
                        self.__conn_handler.send_message_to_node(node_id, msg)
                
                if len(top.acks) == len(self.__all_nodes):
                    msg = self.__delivery_queue.pop()
                    print(f"Nodo-{self.__id}: entregando mensagem com o clock {msg.clock}")
                    self.__on_deliver_cb(self, msg.msg_text)
                else:
                    break
            else:
                break

    def broadcast(self, msg: str):
        self.__send_to_nodes(msg, self.__other_nodes)

    def send(self, node_id, msg: str):
        self.__send_to_nodes(msg, [node_id])

    def receive(self, msg_str: str):
        msg = Message.from_string(msg_str)
        self.__update_clock(new_value=msg.clock)

        if msg.msg_type == MessageType.ACK:
            print(f"Nodo-{self.__id}: recebido ACK de {msg.sender_id} com clock {msg.clock}")
            msg_entry = self.__delivery_queue.find_by_clock(msg.clock)
            if not msg_entry:
                self.__delivery_queue.push(msg)
                msg_entry = msg
            msg_entry.acks.append(msg.sender_id)
        else:
            print(f"Nodo-{self.__id} recebido MESSAGE de {msg.sender_id} com clock {msg.clock}")
            msg_entry = self.__delivery_queue.find_by_clock(msg.clock)
            if msg_entry:
                msg_entry.msg_text = msg.msg_text
            else:
                self.__delivery_queue.push(msg)

        self.__ack_and_deliver()
        
        print(f"Nodo-{self.__id}: mensagens a entregar", self.__delivery_queue.get_stats())

    def exit(self):
        self.__conn_handler.close()