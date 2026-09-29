import sys
import anthropic
from typing import Union

from .base import ChatMessages, ModelResponse, ModelClient

# Claude likes using emojis too much
if sys.stdout and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

target = "anthropic"
class AnthropicClient(ModelClient):
    def __init__(self, model_name: str= "claude-sonnet-4-6", **kwargs):
        super().__init__(model_name, **kwargs)
        api_key = None
        with open("./src/models/keys.txt", "r", encoding="utf-8") as file:
            for line in file:
                if "=" in line:
                    key, val = line.strip().split("=", 1)
            
                    if key.strip() == target:
                        api_key = val.strip()
                        break
        if not api_key:
            raise ValueError("ANTHROPIC API KEY NO AVAILABLE")
        self.client = anthropic.Anthropic(api_key=api_key)
    
    def generate(self, messages: Union[str, ChatMessages], system: str | None = None) -> ModelResponse:
        kwargs = {
            "model": self.model_name,
            "max_tokens": self.max_tokens,
            "messages": self._normalize(messages),
        }
        
        if system:
            kwargs["system"] = system
        
        response = self.client.messages.create(**kwargs)
        
        text = "".join(block.text for block in response.content if block.type == "text")
        
        return ModelResponse (
            text=text,
            model=self.model_name,
            input_token=response.usage.input_tokens,
            output_token=response.usage.output_tokens,
            raw=response.model_dump(),
        )