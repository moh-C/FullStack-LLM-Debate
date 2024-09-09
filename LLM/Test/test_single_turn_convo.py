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

llm1, llm2 = create_persona_llms(debate_topic, name1, name2, provider)

Q1 = "What's your thoughts on buying a lot of stuff from Costco?"
llm1(user_prompt=Q1)
llm2(user_prompt=Q1)

Q2 = "With that question answered, what is your thought on the locations of Costco?"
llm1(user_prompt=Q2)
llm2(user_prompt=Q2)

print(llm1.name, llm1.conversation_history.messages)
print("Next/n")
print(llm2.name, llm2.conversation_history.messages)

print("--"*20)