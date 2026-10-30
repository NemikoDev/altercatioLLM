"""
Orchestrates agents
"""

from typing import List

from agents import Agent, Message
from .algorithm import Algorithm
from state import Transcript
from .answers import extract_answer

class Orchestrator:
    def __init__(self, agents: List[Agent], algorithm: Algorithm, judge: Agent, transcript: Transcript, verbose: bool = True):
        self.agents = agents
        self.algorithm = algorithm
        self.judge = judge
        self.transcript = transcript
        self.verbose = verbose

    def run(self, topic: str) -> Transcript:
        self.algorithm.reset()
        self.transcript.add(Message("Moderator", topic))
        if self.verbose:
            print(f"Moderator: {topic}\n")
        turn = 0
        while not self.algorithm.should_terminate(self.transcript.messages, turn):
            speaker = self.algorithm.select_next_speaker(self.transcript.messages, self.agents, turn)
            reply = speaker.respond(self.transcript.messages)
            reply = self.algorithm.observe(reply)
            self.transcript.add(reply)
            if self.verbose:
                rnd = reply.metadata.get("round")
                tag = f" (round {rnd})" if rnd is not None else ""
                print(f"[{reply.speaker}{tag}] {reply.content}\n")
            turn += 1
        verdict = self.judge.respond(self.transcript.messages)
        verdict.metadata["role"] = "judge"
        verdict.metadata["answer"] = extract_answer(verdict.content)
        self.transcript.add(verdict)
        if self.verbose:
            print(f"[{verdict.speaker}: - FINAL VERDICT] {verdict.content}")
        return self.transcript