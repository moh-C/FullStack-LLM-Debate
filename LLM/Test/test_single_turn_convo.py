import sys, os, json

# Get the parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the parent directory to the system path
sys.path.insert(0, parent_dir)
from utils import create_persona_llms, start_clash

debate_topic = "Buying bulky stuff from Costco"
name1 = "Pete Davidson"
name2 = "Shaq O'Neal"
provider = "openai"

llm1, llm2 = create_persona_llms(debate_topic, name1, name2, provider)

start_clash(
    llm1=llm1,
    llm2=llm2,
    question="What is your take on Costco's giant ass bulky Almonds?",
    turn=3
    )