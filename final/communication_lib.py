import socket
import json

class CommunicationLib:
    def __init__(self, process_id, processes):
        self.process_id = process_id
        self.processes = processes
        self.timestamps = {p: 0 for p in processes}
        self.pending_messages = []

    def send(self, message, destination):
        timestamp = self.increment_timestamp()
        self.pending_messages.append((timestamp, message, destination))
        self.broadcast_pending_messages()

    def receive(self, message):
        timestamp, sender = message['timestamp'], message['sender']
        self.timestamps[sender] = max(self.timestamps[sender], timestamp) + 1
        self.pending_messages.append((timestamp, message, None))
        self.broadcast_pending_messages()

    def broadcast(self, message):
        timestamp = self.increment_timestamp()
        self.pending_messages.append((timestamp, message, None))
        self.broadcast_pending_messages()

    def deliver(self):
        self.pending_messages.sort(key=lambda x: x[0])
        delivered_messages = []
        for _, message, destination in self.pending_messages:
            if destination is None or destination == self.process_id:
                delivered_messages.append(message)
        self.pending_messages = []
        return delivered_messages

    def increment_timestamp(self):
        self.timestamps[self.process_id] += 1
        return self.timestamps[self.process_id]

    def broadcast_pending_messages(self):
        for process in self.processes:
            if process != self.process_id:
                self.send_pending_messages(process)

    def send_pending_messages(self, destination):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.connect(('localhost', destination))
                for _, message, _ in self.pending_messages:
                    data = {
                        'timestamp': self.timestamps[self.process_id],
                        'sender': self.process_id,
                        'message': message
                    }
                    sock.sendall(json.dumps(data).encode())
            except ConnectionRefusedError:
                print(f"Connection refused to process {destination}")

    def start_listening(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(('localhost', self.process_id))
            sock.listen()
            while True:
                conn, addr = sock.accept()
                data = conn.recv(1024).decode()
                if data:
                    message = json.loads(data)
                    self.receive(message)
                conn.close()