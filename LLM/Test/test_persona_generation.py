import os, sys, asyncio

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

from async_utils import generate_debate_personas

async def main():
    debate_topic = "The Impact of Social Media on Society"
    name1 = "Pete Davidson"
    name2 = "Mark Zuckerberg"
    
    try:
        personas = await generate_debate_personas(debate_topic, name1, name2)
        
        print(f"Generated personas for the debate topic: {debate_topic}\n")
        
        for i, persona in enumerate(personas, 1):
            print(f"Persona {i}:")
            print(f"Name: {persona['name']}")
            print(f"System Prompt: {persona['system_prompt']}")
            print()
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())