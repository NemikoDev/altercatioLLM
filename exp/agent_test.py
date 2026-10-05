import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))

from agents import Agent, Message
from models import AnthropicClient, OpenAIClient


def build_clients():
    clients = []
    for cls in (AnthropicClient, OpenAIClient):
        try:
            clients.append(cls())
        except Exception as e:
            print(f"[skip] {cls.__name__}: {e}")
    if not clients:
        raise SystemExit("No API keys set")
    if len(clients) == 1:
        clients.append(clients[0])
    return clients


def main():
    a_client, b_client = build_clients()

    optimist = Agent("Optimist", "You argue that the idea under discussion is promising and highlight upsides.", a_client)
    skeptic = Agent("Skeptic", "You challenge weak assumptions and point out risks and failure modes.", b_client)

    transcript = [Message("Moderator", "Topic: What is the fastest way to approach inifinity in mathematics?")]

    for _ in range(3):
        for agent in (optimist, skeptic):
            reply = agent.respond(transcript)
            transcript.append(reply)
            print(f"\n[{reply.speaker}]\n{reply.content}")


if __name__ == "__main__":
    main()