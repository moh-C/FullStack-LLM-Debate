"""
Utilities for generating and managing debate personas and conversations.

This module provides functions and classes for creating debate personas,
managing conversation history, and facilitating debates between AI agents.
"""

import re
import os
import json
from datetime import datetime
from typing import List, Tuple, Dict, Literal
from dataclasses import dataclass

from base import LLM
from prompts.Persona import SET_PERSONA
from prompts.clash import DEBATE_PERSONA

CACHE_DIR = "debate_personas_cache"


@dataclass
class Message:
    """
    Represents a message in the conversation history.

    Attributes:
        role (str): The role of the message sender.
        content (str): The content of the message.
        timestamp (datetime): The time the message was created.
        is_summary (bool): Whether the message is a summary.
        is_question (bool): Whether the message is a question.
        turn (int): The turn number of the message in the conversation.
    """

    role: str
    content: str
    timestamp: datetime
    is_summary: bool = False
    is_question: bool = False
    turn: int = 0


class ConversationHistory:
    """
    Manages the conversation history for a debate.

    Attributes:
        messages (List[Message]): List of messages in the conversation.
        max_messages (int): Maximum number of messages to keep in history.
        summarizer (LLM): LLM instance used for generating summaries.
        summary_interval (int): Number of turns between summaries.
        turn_count (int): Current turn count in the conversation.
    """

    def __init__(
        self,
        summarizer: LLM,
        max_messages: int = 15,
        summary_interval: int = 5
    ):
        """
        Initialize the ConversationHistory.

        Args:
            summarizer (LLM): LLM instance used for generating summaries.
            max_messages (int): Maximum number of messages to keep in history.
            summary_interval (int): Number of turns between summaries.
        """
        self.messages: List[Message] = []
        self.max_messages = max_messages
        self.summarizer = summarizer
        self.summary_interval = summary_interval
        self.turn_count = 0

    def add_question(self, question: str) -> None:
        """
        Add a question to the conversation history.

        Args:
            question (str): The question to add.
        """
        self.turn_count += 1
        self.messages.append(
            Message(
                "Question",
                question,
                datetime.now(),
                is_question=True,
                turn=self.turn_count
            )
        )

    def add_message(self, role: str, content: str) -> None:
        """
        Add a message to the conversation history.

        Args:
            role (str): The role of the message sender.
            content (str): The content of the message.
        """
        self.messages.append(
            Message(role, content, datetime.now(), turn=self.turn_count)
        )
        if len(self.messages) > self.max_messages:
            self.messages = (
                [msg for msg in self.messages if msg.is_summary]
                + self.messages[-self.max_messages:]
            )
        if self.turn_count % self.summary_interval == 0:
            self._generate_summary()

    def get_history(self) -> str:
        """
        Get a formatted string of the conversation history.

        Returns:
            str: Formatted conversation history.
        """
        formatted_history = []
        current_turn = 0
        for msg in self.messages:
            if msg.is_summary:
                formatted_history.append(f"Summary: {msg.content}\n")
            elif msg.is_question:
                formatted_history.extend([
                    f"Question: {msg.content}",
                    f"Turn: {msg.turn}"
                ])
                current_turn = msg.turn
            elif msg.turn == current_turn:
                formatted_history.append(f"{msg.role}: {msg.content}")
        return "\n".join(formatted_history)

    def _generate_summary(self) -> None:
        """Generate a summary of the conversation and add it to the history."""
        context = "\n".join(
            f"{msg.role}: {msg.content}"
            for msg in self.messages
            if not msg.is_summary
        )
        summary_prompt = (
            f"Summarize the following conversation concisely, "
            f"capturing the main points:\n\n{context}\n\nSummary:"
        )
        summary = self.summarizer(summary_prompt)
        self.messages = (
            [msg for msg in self.messages if msg.is_summary]
            + [Message("Summary", summary, datetime.now(), is_summary=True)]
        )


def extract_persona_data(xml_string: str) -> List[Dict[str, str]]:
    """
    Extract persona data from an XML string.

    Args:
        xml_string (str): XML string containing persona data.

    Returns:
        List[Dict[str, str]]: List of dictionaries containing persona data.
    """
    personas = []
    persona_pattern = (
        r'<persona>\s*<name>(.*?)</name>\s*<userprompt>(.*?)</userprompt>'
        r'\s*<systemprompt>(.*?)</systemprompt>\s*</persona>'
    )
    matches = re.findall(persona_pattern, xml_string, re.DOTALL)
    
    for match in matches:
        name, user_prompt, system_prompt = match
        user_prompt = re.sub(r'\s+', ' ', user_prompt).strip()
        system_prompt = re.sub(r'\s+', ' ', system_prompt).strip()
        user_prompt = re.sub(
            r'<conversation_history>.*?</conversation_history>',
            '',
            user_prompt
        ).strip()
        
        personas.append({
            'name': name.strip(),
            'user_prompt': user_prompt,
            'system_prompt': system_prompt
        })
    
    return personas


def generate_debate_personas(
    debate_topic: str,
    name1: str,
    name2: str,
    answer_length: int = 250,
    provider: Literal["openai", "claude"] = "openai"
) -> Tuple[Dict[str, str], Dict[str, str]]:
    """
    Generate debate personas based on the given topic and names.

    Args:
        debate_topic (str): The topic of the debate.
        name1 (str): Name of the first debater.
        name2 (str): Name of the second debater.
        answer_length (int): Length of the debate per turn.
        provider (Literal["openai", "claude"]): The LLM provider to use.

    Returns:
        Tuple[Dict[str, str], Dict[str, str]]: Two dictionaries containing
        the name, user prompt, and system prompt for each persona.
    """
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_key = f"{debate_topic}_{name1}_{name2}_{provider}".replace(" ", "_")
    cache_file = os.path.join(CACHE_DIR, f"{cache_key}.json")

    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            return tuple(json.load(f))

    prompt = SET_PERSONA.format(
        debate_topic=debate_topic,
        name1=name1,
        name2=name2,
        answer_length=answer_length
    )

    llm = LLM(provider=provider, stream=False)
    response = llm(user_prompt=prompt)
    personas = extract_persona_data(response)

    if len(personas) != 2:
        raise ValueError(f"Expected 2 personas, but got {len(personas)}")

    result = tuple(
        {
            "name": persona["name"],
            "user_prompt": persona["user_prompt"],
            "system_prompt": persona["system_prompt"]
        }
        for persona in personas
    )

    with open(cache_file, 'w') as f:
        json.dump(result, f)

    return result


def create_persona_llms(
    debate_topic: str,
    name1: str,
    name2: str,
    provider: Literal["openai", "claude"] = "openai",
    stream: bool = True,
    max_tokens: int = 400,
    temperature: float = 0.7
) -> Tuple[LLM, LLM]:
    """
    Create LLM objects for two debate personas.

    Args:
        debate_topic (str): The topic of the debate.
        name1 (str): Name of the first debater.
        name2 (str): Name of the second debater.
        provider (Literal["openai", "claude"]): The LLM provider to use.
        stream (bool): Whether to enable streaming for the LLMs.
        max_tokens (int): Maximum number of tokens for LLM responses.
        temperature (float): Temperature setting for the LLMs.

    Returns:
        Tuple[LLM, LLM]: Two LLM objects, one for each persona.
    """
    persona1, persona2 = generate_debate_personas(
        debate_topic, name1, name2, provider
    )

    llm1 = LLM(
        provider=provider,
        name=persona1["name"],
        stream=stream,
        max_tokens=max_tokens,
        temperature=temperature,
        system_prompt=persona1["system_prompt"]
    )

    llm2 = LLM(
        provider=provider,
        name=persona2["name"],
        stream=stream,
        max_tokens=max_tokens,
        temperature=temperature,
        system_prompt=persona2["system_prompt"]
    )

    return llm1, llm2


def start_clash(llm1: LLM, llm2: LLM, question: str, turn: int = 5) -> None:
    """
    Start a debate clash between two LLM personas.

    Args:
        llm1 (LLM): First LLM persona.
        llm2 (LLM): Second LLM persona.
        question (str): The debate question.
        turn (int): Number of turns in the debate.
    """
    summarizer = LLM(provider="claude", stream=False)
    history = ConversationHistory(summarizer, max_messages=15, summary_interval=5)
    
    debate_topic = "Buying bulky stuff from Costco"
    name1 = llm1.name
    name2 = llm2.name

    history.add_question(question=question)

    for persona_llm in (llm1, llm2):
        response = persona_llm(user_prompt=question)
        history.add_message(persona_llm.name, response)
    
    history.add_message("Info", "-------------------Turn DONE------------------")

    for _ in range(turn):
        for persona_llm, opponent_name in ((llm1, name2), (llm2, name1)):
            debate_prompt = DEBATE_PERSONA.format(
                name=persona_llm.name,
                opponent=opponent_name,
                debate_topic=debate_topic,
                question=question,
                history=history.get_history(),
                answer_length=150
            )
            response = persona_llm(user_prompt=debate_prompt)
            response_match = re.search(r'<response>(.*?)</response>', response, re.DOTALL)
            generated_response = response_match.group(1).strip()
            history.add_message(persona_llm.name, generated_response)

        history.add_message("Info", "-------------------Turn DONE------------------")

    print("Conversation History:")
    print(history.get_history())
    print("\nDone")