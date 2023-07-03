from message import Message

class PriorityQueue:
    # using list
    def __init__(self, max_size=100):
        self.heap = []

    def find_by_lc(self, lc):
        # find a message by its Lamport Clock
        for msg in self.heap:
            if msg.lc == lc:
                return msg

    def push(self, msg: Message):
        self.heap.append(msg)
        self.heap.sort(key=lambda x: x.lc, reverse=True)  # smallest at the end

    def pop(self):
        msg = self.heap.pop()
        return msg

    def get_stats(self):
        # list of (lc, acks)
        return [(msg.lc, msg.acks) for msg in self.heap]

    @property
    def top(self):
        return self.heap[-1] if self.heap else None
