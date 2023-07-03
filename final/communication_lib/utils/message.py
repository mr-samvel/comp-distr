from dataclasses import dataclass, field
from enum import EnumMeta

class MessageType(EnumMeta):
    MESSAGE = "MESSAGE"
    ACK = "ACK"

@dataclass
class Message:
    lc: int  # identifier
    msg_type: MessageType
    sender: int
    msg_text: str = None
    acks: list = field(default_factory=set)  # internal use, for queue

    def __repr__(self) -> str:
        return f"{self.lc};{self.msg_type};{self.sender};{self.msg_text}"

    @classmethod
    def from_string(cls, msg_str):
        lc, msg_type, sender, msg_text = msg_str.split(";")
        return cls(lc=float(lc), msg_type=msg_type, sender=int(sender), msg_text=msg_text)