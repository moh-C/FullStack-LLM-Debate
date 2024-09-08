from base import LLM
import os
print(os.getcwd())

from prompts.Persona import SET_PERSONA
from utils import extract_persona_data

debate_topic = "Buying bulky stuff from Costco"
name1 = "Pete Davidson"
name2 = "Shaq O'Neal"

prompt = SET_PERSONA.format(
    debate_topic=debate_topic,
    name1=name1,
    name2=name2
)

# For OpenAI
llm1 = LLM(provider="openai", stream=False)
response1 = llm1(prompt=prompt)
personas = extract_persona_data(response1)

for persona in personas:
    print(f"Name: {persona['name']}")
    print(f"User Prompt: {persona['user_prompt']}")
    print(f"System Prompt: {persona['system_prompt']}")
    print()

print("/n/n/n")

# For Claude
llm2 = LLM(provider="claude", stream=False)
response2 = llm2(prompt=prompt)
personas = extract_persona_data(response2)

for persona in personas:
    print(f"Name: {persona['name']}")
    print(f"User Prompt: {persona['user_prompt']}")
    print(f"System Prompt: {persona['system_prompt']}")
    print()

print("/n/n/n")