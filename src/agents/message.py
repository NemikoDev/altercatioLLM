from dataclasses import dataclass



@dataclass
class Message:
    speaker: str
    content: str