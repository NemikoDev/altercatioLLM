"""
Shared record of the messages between agents
"""


import json
from dataclasses import asdict
from pathlib import Path
from typing import List, Optional

from agents import Message



class Transcript:
    def __init__(self, log_path: Optional[Path] = None):
        self.messages: List[Message] = []
        self.log_path = Path(log_path) if log_path else None
        if self.log_path:
            self.log_path.parent.mkdir(parents=True, exist_ok=True)
            self.log_path.write_text("", encoding="utf-8")
    
    def add(self, message: Message) -> None:
        self.messages.append(message)
        if self.log_path:
            with self.log_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(asdict(message), ensure_ascii=False) + "\n")