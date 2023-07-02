from queue import Queue
from collections import defaultdict

class CommunicationLib:
    def __init__(self, num_processes):
        self.num_processes = num_processes
        self.message_queue = Queue()
        self.pending_messages = defaultdict(list)
        self.process_clock = [0] * num_processes

    def send(self, recipient_id, msg):
        timestamp = self.increment_clock(recipient_id)
        self.pending_messages[recipient_id].append((timestamp, msg))

    def receive(self, msg):
        self.message_queue.put(msg)
        self.process_pending_messages()

    def broadcast(self, msg):
        timestamp = self.increment_clock()
        self.pending_messages['broadcast'].append((timestamp, msg))
        self.process_pending_messages()

    def deliver(self, msg):
        self.message_queue.put(msg)
        self.process_pending_messages()

    def process_pending_messages(self):
        while not self.message_queue.empty():
            msg = self.message_queue.get()

            if isinstance(msg, tuple):
                timestamp, content = msg
                self.process_clock[timestamp[0]] = max(
                    self.process_clock[timestamp[0]], timestamp[1]
                )
            else:
                content = msg

            # Process messages intended for a specific recipient
            if content['type'] == 'unicast':
                recipient_id = content['recipient_id']
                if recipient_id != 'broadcast':
                    if self.can_deliver(content['timestamp']):
                        self.message_queue.put(content['message'])
            # Process broadcast messages
            elif content['type'] == 'broadcast':
                if self.can_deliver(content['timestamp']):
                    self.message_queue.put(content['message'])

    def can_deliver(self, timestamp):
        process_id, timestamp_value = timestamp
        return self.process_clock[process_id] == timestamp_value - 1

    def increment_clock(self, process_id=None):
        if process_id is None:
            process_id = 'broadcast'
        self.process_clock[process_id] += 1
        return (process_id, self.process_clock[process_id])