from dataclasses import dataclass
from datetime import datetime
from typing import List
import sys, os, json

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
from base import LLM
from utils import ConversationHistory, create_persona_llms

# Usage example
if __name__ == "__main__":
    from utils import create_persona_llms
    
    summarizer = LLM(provider="claude", stream=False)
    history = ConversationHistory(summarizer, max_messages=15, summary_interval=5)
    
    debate_topic = "Buying bulky stuff from Costco"
    name1 = "Pete Davidson"
    name2 = "Shaq O'Neal"
    provider = "openai"

    llm1, llm2 = create_persona_llms(debate_topic, name1, name2, provider)

    Q1 = "What's your thoughts on buying a lot of stuff from Costco?"
    history.add_question(Q1)

    response_llm1 = llm1(user_prompt=Q1)
    history.add_message(name1, response_llm1)

    response_llm2 = llm2(user_prompt=Q1)
    history.add_message(name2, response_llm2)

    print("Conversation History:")
    print(history.get_history())

    print("\nDone")