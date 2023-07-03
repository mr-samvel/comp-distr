from dataclasses import dataclass, field
from enum import EnumMeta

class MessageType(EnumMeta):
    MESSAGE = "MESSAGE"
    ACK = "ACK"

@dataclass
class Message:
    clock: int  # identificador
    msg_type: MessageType
    sender_id: int
    msg_text: str = None
    acks: list = field(default_factory=set)

    def __repr__(self) -> str:
        return f"{self.clock};{self.msg_type};{self.sender_id};{self.msg_text}"

    @classmethod
    def from_string(cls, msg: str):
        clock, msg_type, sender, msg_text = msg.split(";")
        return cls(clock=float(clock), msg_type=msg_type, sender=int(sender), msg_text=msg_text)