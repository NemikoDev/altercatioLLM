from openai import OpenAI
from typing import Union
from .base import ChatMessages, ModelClient, ModelResponse

target = "openai"
class OpenAIClient(ModelClient):
    def __init__(self, model_name: str = "gpt-4o", **kwargs):
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
            raise ValueError("OPENAI API KEY NOT AVAILABLE")
        self.client = OpenAI(api_key=api_key)
        
    def generate(self,  messages: Union[str, ChatMessages], system: str | None = None) -> ModelResponse:
        chat = []
        
        if system:
            chat.append({"role": "system", "content": system})
        chat.extend(self._normalize(messages))
        
        response = self.client.chat.completions.create(
            model=self.model_name,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            messages=chat,
        )
        
        choice=response.choices[0]
        
        return ModelResponse(
            text=choice.message.content,
            model=self.model_name,
            input_token=response.usage.prompt_tokens,
            output_token=response.usage.completion_tokens,
            raw=response.model_dump(),
        )