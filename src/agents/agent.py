from models import ModelClient
from .message import Message
from typing import List




# Initialize Agent class. Contains personality, will consume transcript
class Agent:
    def __init__(self, name: str, persona: str, client: ModelClient):
        self.name = name
        self.persona = persona
        self.client = client

    def system_prompt(self) -> str:
        return (
            f"You are {self.name}, one participant in a multi-party discussion.\n"
            f"{self.persona}\n\n"
            "Messages from other participants appear prefixed with their name in "
            "square brackets, e.g. [Alice]: ... Do NOT prefix your own reply with "
            "your name; just write your contribution. Keep it concise."
        )

    def render_view(self, transcript: List[Message]) -> List[dict]:
        msgs: List[dict] = []
        for m in transcript:
            if m.speaker == self.name:
                role, content = "assistant", m.content
            else:
                role, content = "user", f"[{m.speaker}]: {m.content}"

            if msgs and msgs[-1]["role"] == role:
                msgs[-1]["content"] += "\n\n" + content
            else:
                msgs.append({"role": role, "content": content})

        if not msgs and msgs[0]["role"] != "user":
            msgs.insert(0, {"role": "user", "content": "[Moderator]: The discussion begins."})
        if msgs[-1]["role"] != "user":
            msgs.append({"role": "user", "content": "[Moderator]: Please continue."})
        return msgs

    def respond(self, transcript: List[Message]) -> Message:
        response = self.client.generate(self.render_view(transcript), system=self.system_prompt())
        text = response.text.strip()

        prefix = f"[{self.name}]: "
        if text.startswith(prefix):
            text = text[len(prefix):].strip()

        return Message(speaker=self.name, content=text)