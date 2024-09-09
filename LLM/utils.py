import re, os
from base import LLM
import json
from typing import Literal, Tuple, Dict
from prompts.Persona import SET_PERSONA
from prompts.clash import DEBATE_PERSONA
from dataclasses import dataclass
from datetime import datetime
from typing import List

CACHE_DIR = "debate_personas_cache"

def extract_persona_data(xml_string):
    personas = []
    
    # Pattern to match each persona block
    persona_pattern = r'<persona>\s*<name>(.*?)</name>\s*<userprompt>(.*?)</userprompt>\s*<systemprompt>(.*?)</systemprompt>\s*</persona>'
    
    # Find all matches
    matches = re.findall(persona_pattern, xml_string, re.DOTALL)
    
    for match in matches:
        name, user_prompt, system_prompt = match
        
        # Clean up the prompts
        user_prompt = re.sub(r'\s+', ' ', user_prompt).strip()
        system_prompt = re.sub(r'\s+', ' ', system_prompt).strip()
        
        # Remove the conversation_history tags from user_prompt
        user_prompt = re.sub(r'<conversation_history>.*?</conversation_history>', '', user_prompt).strip()
        
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
        answer_length (int): Length of the debate per turn,
        provider (Literal["openai", "claude"]): The LLM provider to use.

    Returns:
        Tuple[Dict[str, str], Dict[str, str]]: Two dictionaries containing
        the name, user prompt, and system prompt for each persona.
    """
        # Create cache directory if it doesn't exist
    os.makedirs(CACHE_DIR, exist_ok=True)

    # Create a cache key and file path
    cache_key = f"{debate_topic}_{name1}_{name2}_{provider}".replace(" ", "_")
    cache_file = os.path.join(CACHE_DIR, f"{cache_key}.json")
    print(f"Cache file is {cache_file}")

    # Try to get cached result
    if os.path.exists(cache_file):
        print(f"Opening cache file")
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
    
    print("Raw LLM response:")
    print(response)
    
    personas = extract_persona_data(response)

    print(f"Extracted personas: {len(personas)}")
    for i, persona in enumerate(personas):
        print(f"Persona {i+1}:")
        print(json.dumps(persona, indent=2))

    if len(personas) != 2:
        raise ValueError(f"Expected 2 personas, but got {len(personas)}")

    if len(personas) < 2:
        raise ValueError("Not enough personas generated")

    persona1 = {
        "name": personas[0]["name"],
        "user_prompt": personas[0]["user_prompt"],
        "system_prompt": personas[0]["system_prompt"]
    }

    persona2 = {
        "name": personas[1]["name"],
        "user_prompt": personas[1]["user_prompt"],
        "system_prompt": personas[1]["system_prompt"]
    }

    result = (persona1, persona2)

    # Cache the result
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
    # Generate personas
    persona1, persona2 = generate_debate_personas(debate_topic, name1, name2, provider)

    # Create LLM for Persona 1
    llm1 = LLM(
        provider=provider,
        name=persona1["name"],
        stream=stream,
        max_tokens=max_tokens,
        temperature=temperature,
        system_prompt=persona1["system_prompt"]
    )

    # Create LLM for Persona 2
    llm2 = LLM(
        provider=provider,
        name=persona2["name"],
        stream=stream,
        max_tokens=max_tokens,
        temperature=temperature,
        system_prompt=persona2["system_prompt"]
    )

    return llm1, llm2

@dataclass
class Message:
    role: str
    content: str
    timestamp: datetime
    is_summary: bool = False
    is_question: bool = False
    turn: int = 0

class ConversationHistory:
    def __init__(self, summarizer: LLM, max_messages: int = 15, summary_interval: int = 5):
        self.messages: List[Message] = []
        self.max_messages = max_messages
        self.summarizer = summarizer
        self.summary_interval = summary_interval
        self.turn_count = 0

    def add_question(self, question: str):
        self.turn_count += 1
        self.messages.append(Message("Question", question, datetime.now(), is_question=True, turn=self.turn_count))

    def add_message(self, role: str, content: str):
        self.messages.append(Message(role, content, datetime.now(), turn=self.turn_count))
        if len(self.messages) > self.max_messages:
            self.messages = [msg for msg in self.messages if msg.is_summary] + self.messages[-self.max_messages:]
        if self.turn_count % self.summary_interval == 0:
            self._generate_summary()

    def get_history(self) -> str:
        formatted_history = ""
        current_turn = 0
        for msg in self.messages:
            if msg.is_summary:
                formatted_history += f"Summary: {msg.content}\n\n"
            elif msg.is_question:
                formatted_history += f"Question: {msg.content}\n"
                formatted_history += f"Turn: {msg.turn}\n"
                current_turn = msg.turn
            elif msg.turn == current_turn:
                formatted_history += f"{msg.role}: {msg.content}\n"
        return formatted_history.strip()

    def _generate_summary(self):
        context = "\n".join([f"{msg.role}: {msg.content}" for msg in self.messages if not msg.is_summary])
        summary_prompt = f"Summarize the following conversation concisely, capturing the main points:\n\n{context}\n\nSummary:"
        summary = self.summarizer(summary_prompt)
        self.messages = [msg for msg in self.messages if msg.is_summary] + [Message("Summary", summary, datetime.now(), is_summary=True)]


def start_clash(llm1, llm2, question, turn=5):
    summarizer = LLM(provider="claude", stream=False)
    history = ConversationHistory(summarizer, max_messages=15, summary_interval=5)
    
    debate_topic = "Buying bulky stuff from Costco"
    name1 = "Pete Davidson"
    name2 = "Shaq O'Neal"
    provider = "openai"

    llm1, llm2 = create_persona_llms(debate_topic, name1, name2, provider)

    history.add_question(question=question)

    response_llm1 = llm1(user_prompt=question)
    history.add_message(name1, response_llm1)

    response_llm2 = llm2(user_prompt=question)
    history.add_message(name2, response_llm2)
    history.add_message("Info", f"-------------------Turn DONE------------------")

    for _ in range(turn):
        debate_prompt = DEBATE_PERSONA.format(
            name=name1,
            opponent=name2,
            debate_topic=debate_topic,
            question=question,
            history=history.get_history(),
            answer_length=150
        )
        response_llm1 = llm1(user_prompt=debate_prompt)
        response_match = re.search(r'<response>(.*?)</response>', response_llm1, re.DOTALL)
        generated_response1 = response_match.group(1).strip()
        history.add_message(name1, generated_response1)

        
        debate_prompt = DEBATE_PERSONA.format(
            name=name2,
            opponent=name1,
            debate_topic=debate_topic,
            question=question,
            history=history.get_history(),
            answer_length=150
        )
        response_llm2 = llm2(user_prompt=debate_prompt)
        response_match = re.search(r'<response>(.*?)</response>', response_llm2, re.DOTALL)
        generated_response2 = response_match.group(1).strip()
        history.add_message(name2, generated_response2)

        history.add_message("Info", "-------------------Turn DONE------------------")


    print("Conversation History:")
    print(history.get_history())

    print("\nDone")
