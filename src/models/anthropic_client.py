import os
import anthropic

from .base import ModelResponse, ModelClient

class AnthropicClient(ModelClient):
    def __init__(self, model_name: str= "claude-sonnet-4-6", **kwargs):
        super().__init__(model_name, **kwargs)
        api_key = os.environ.get("ANTHROPIC_API")
        if not api_key:
            raise ValueError("ANTHROPIC API KEY NO AVAILABLE")
        self.client = anthropic.Anthropic(api_key=api_key)
    
    def generate(self, prompt: str, system: str | None = None) -> ModelResponse:
        kwargs = {
            "model": self.model_name,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "messages": [{"role": "user", "content": prompt}]
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