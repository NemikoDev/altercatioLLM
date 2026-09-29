from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Union

"""abstract interface client for models"""

ChatMessages = List[Dict[str, str]]

@dataclass
class ModelResponse:
    text:str
    model:str
    input_token:int | None = None
    output_token:int | None = None
    raw: dict | None = None
    

class ModelClient(ABC):
    def __init__(self, model_name: str, temperature: float = 0.7, max_tokens: int = 1024):
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        
    @staticmethod
    def _normalize(messages: Union[str, ChatMessages]) -> ChatMessages:
        if isinstance(messages, str):
            return [{"role": "user", "content": messages}]
        return messages
        
    @abstractmethod
    def generate(self, prompt: str, system: str | None = None) -> ModelResponse:
        raise NotImplementedError