from datetime import datetime
from typing import List, Tuple, Optional
from dataclasses import dataclass
from base import AsyncLLM
import tiktoken

@dataclass
class Message:
    content: str
    timestamp: datetime
    sender: str
    is_summary: bool = False

class ConversationHistory:
    def __init__(
        self,
        summarizer: AsyncLLM,
        max_token_length: int = 2000
    ):
        self.messages: List[Message] = []
        self.summarizer = summarizer
        self.max_token_length = max_token_length
        self.encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

    async def add_message(self, content: str, sender: str) -> None:
        new_message = Message(content, datetime.now(), sender)
        self.messages.append(new_message)
        
        if self._get_token_count() > self.max_token_length:
            await self._generate_summary()

    def get_last_messages(self, current_llm: str, opponent_llm: str) -> List[Tuple[str, Optional[Message]]]:
        current_llm_msg = next((msg for msg in reversed(self.messages) if msg.sender == current_llm), None)
        opponent_llm_msg = next((msg for msg in reversed(self.messages) if msg.sender == opponent_llm), None)
        return [(current_llm, current_llm_msg), (opponent_llm, opponent_llm_msg)]

    def get_history(self) -> str:
        return "\n".join(f"{msg.sender}: {msg.content}" for msg in self.messages)

    def _get_token_count(self) -> int:
        return sum(len(self.encoding.encode(msg.content)) for msg in self.messages)

    async def _generate_summary(self) -> None:
        context = "\n".join(f"{msg.sender}: {msg.content}" for msg in self.messages if not msg.is_summary)
        summary_prompt = f"Summarize the following conversation concisely:\n\n{context}\n\nSummary:"
        
        summary_content = ""
        async for chunk in self.summarizer(summary_prompt):
            summary_content += chunk
        
        summary_message = Message(summary_content, datetime.now(), "Summary", is_summary=True)
        self.messages = [msg for msg in self.messages if msg.is_summary] + [summary_message]
