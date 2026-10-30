"""
round-robin implementation of the adaptive orchestration strategy.
"""


from typing import List

from agents import Agent, Message
from .algorithm import Algorithm


class AdaptiveDebate(Algorithm):
    def __init__(self, skeptic_name: str, agents_per_round: int = 2, min_rounds: int = 1, max_rounds: int = 3):
        self.skeptic_name = skeptic_name
        self.agents_per_round = agents_per_round
        self.min_turns = min_rounds
        self.max_turns = max_rounds
        self._agreed = False
        
        
    def reset(self) -> None:
        self._agreed = False

    def select_next_speaker(self, transcript: List[Message], agents: List[Agent], turn: int) -> Agent:
        return agents[turn % len(agents)]
    
    def observe(self, message: Message) -> Message:
        if message.speaker == self.skeptic_name:
            lines = message.content.splitlines()
            if lines and lines[0].strip().upper().startswith("AGREEMENT:"):
                flag = lines[0].strip().split(":", 1)[1].strip().upper()
                self._agreed = flag == "YES"
                message.content = "\n".join(lines[1:]).strip()
                message.metadata["agreement"] = self._agreed
        return message

    def should_terminate(self, transcript: List[Message], turn: int) -> bool:
        if turn >= self.max_turns:
            return True
        if turn >= self.min_turns and self._agreed:
            return True
        return False