from dataclasses import dataclass
from datetime import datetime
from typing import List
import sys, os, json

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
from base import LLM

@dataclass
class Message:
    role: str
    content: str
    timestamp: datetime
    is_summary: bool = False

class ConversationHistory:
    def __init__(self, llm: LLM, max_messages: int = 10, summary_interval: int = 5):
        self.messages: List[Message] = []
        self.max_messages = max_messages
        self.llm = llm
        self.summary_interval = summary_interval
        self.turn_count = 0

    def add_message(self, role: str, content: str):
        self.messages.append(Message(role, content, datetime.now()))
        self.turn_count += 1
        if len(self.messages) > self.max_messages:
            self.messages.pop(0)
        if self.turn_count % self.summary_interval == 0:
            self._generate_summary()

    def get_prompt(self, system_prompt: str, current_query: str) -> str:
        context = "\n".join([f"{'Summary' if msg.is_summary else msg.role}: {msg.content}" for msg in self.messages])
        return f"{system_prompt}\n\nConversation history:\n{context}\n\nCurrent query: {current_query}\n"

    def get_response(self, system_prompt: str, user_query: str) -> str:
        prompt = self.get_prompt(system_prompt, user_query)
        response = self.llm(prompt)
        self.add_message("user", user_query)
        self.add_message("assistant", response)
        return response

    def _generate_summary(self):
        context = "\n".join([f"{msg.role}: {msg.content}" for msg in self.messages if not msg.is_summary])
        summary_prompt = f"Summarize the following conversation concisely, capturing the main points:\n\n{context}\n\nSummary:"
        summary = self.llm(summary_prompt)
        self.messages = [msg for msg in self.messages if msg.is_summary] + [Message("system", summary, datetime.now(), is_summary=True)]

# Usage example
if __name__ == "__main__":
    llm = LLM(provider="claude", stream=False)
    history = ConversationHistory(llm, max_messages=15, summary_interval=5)
    
    system_prompt = "You are a helpful AI assistant."
    
    for i in range(7):
        user_query = f"This is question {i+1}. Please provide a short response."
        response = history.get_response(system_prompt, user_query)
        print(f"User: {user_query}")
        print(f"Assistant: {response}\n")
    
    print("Final conversation state:")
    for msg in history.messages:
        print(f"{'Summary' if msg.is_summary else msg.role}: {msg.content}")