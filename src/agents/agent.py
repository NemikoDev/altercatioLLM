from models import ModelClient




# Initialize Agent class. Contains personality, will consume transcript
class Agent:
    def __init__(self, name: str, persona: str, client: ModelClient):
        self.name = name
        self.persona = persona
        self.client = client
    