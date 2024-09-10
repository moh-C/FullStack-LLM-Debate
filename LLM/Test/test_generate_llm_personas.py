import sys, os, json
import asyncio

# Get the parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the parent directory to the system path
sys.path.insert(0, parent_dir)
from async_utils import create_persona_llms

debate_topic = "Buying bulky stuff from Costco"
name1 = "Pete Davidson"
name2 = "Shaq O'Neal"
provider = "openai"

async def main():
    debate_topic = "The Impact of Social Media on Society"
    name1 = "Pete Davidson"
    name2 = "Mark Zuckerberg"
    
    try:
        llm1, llm2 = await create_persona_llms(debate_topic, name1, name2)
        
        print(f"Generated LLMs for the debate topic: {debate_topic}\n")
        
        for i, llm in enumerate([llm1, llm2], 1):
            print(f"LLM {i}:")
            print(f"Name: {llm.name}")
            print(f"Provider: {llm.provider}")
            print(f"System Prompt: {llm.system_prompt}")
            print()
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())