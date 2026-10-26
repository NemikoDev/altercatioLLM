"""
algo abstract interface. Used for orchestration.
"""

from abc import ABC, abstractmethod
from typing import List

from agents import Agent, Message


class Algorithm(ABC):
    @abstractmethod
    def select_next_speaker(self, transcript: List[Message], agents: List[Agent], turn: int) -> Agent:
        raise NotImplementedError
    
    @abstractmethod
    def should_terminate(self, transcript: List[Message], turn: int) -> bool:
        raise NotImplementedError
    
    def observe(self, message: Message) -> Message:
        return message