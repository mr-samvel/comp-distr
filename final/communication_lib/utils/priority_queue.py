from typing import List, Tuple, Union
from .message import Message

class MessagePriorityQueue:
    # using list
    def __init__(self, max_size=100):
        self.heap: List[Message] = []

    def find_by_clock(self, clock) -> Message:
        for msg in self.heap:
            if msg.clock == clock:
                return msg

    def push(self, msg: Message) -> None:
        self.heap.append(msg)
        self.heap.sort(key=lambda x: x.clock, reverse=True)  # smallest at the end

    def pop(self) -> Message:
        msg = self.heap.pop()
        return msg

    def get_stats(self) -> List[Tuple[int, list]]:
        return [(msg.clock, msg.acks) for msg in self.heap]

    @property
    def top(self) -> Union[Message, None]:
        return self.heap[-1] if self.heap else None
