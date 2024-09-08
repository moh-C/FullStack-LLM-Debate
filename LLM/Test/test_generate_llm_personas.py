import sys, os, json

# Get the parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the parent directory to the system path
sys.path.insert(0, parent_dir)
from utils import create_persona_llms

debate_topic = "Buying bulky stuff from Costco"
name1 = "Pete Davidson"
name2 = "Shaq O'Neal"
provider = "openai"

try:
    llm_pete, llm_shaq = create_persona_llms(debate_topic, name1, name2, provider)

    # Test the LLMs
    pete_response = llm_pete("What do you think about buying in bulk from Costco?")
    shaq_response = llm_shaq("What's your opinion on Costco's large quantities?")

    print(f"{name1}'s response:")
    print(pete_response)
    print(f"\n{name2}'s response:")
    print(shaq_response)

except Exception as e:
    print(f"An error occurred: {str(e)}")