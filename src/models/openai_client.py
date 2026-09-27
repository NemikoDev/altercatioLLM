import os
from openai import OpenAI

from .base import ModelClient,ModelResponse


class OpenAIClient(ModelClient):
    def __init__(self, model_name: str = "gpt-4o", **kwargs):
        super().__init__(model_name, **kwargs)
        api_key = os.environ.get("OPENAI_API")
        if not api_key:
            raise ValueError("OPENAI API KEY NOT AVAILABLE")
        self.client = OpenAI(api_key=api_key)
        
    def generate(self, prompt: str, system: str | None = None) -> ModelResponse:
        messages = []
        
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        
        response = self.client.chat.completions.create(
            model=self.model_name,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            messages=messages,
        )
        
        choice=response.choices[0]
        
        return ModelResponse(
            text=choice.messsage.content,
            model=self.model_name,
            input_token=response.usage.prompt_tokens,
            output_token=response.usage.completion_tokens,
            raw=response.model_dump(),
        )