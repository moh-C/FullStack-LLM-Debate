import os, sys

# Get the parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the parent directory to the system path
sys.path.insert(0, parent_dir)

from utils import generate_debate_personas

debate_topic = "Buying bulky stuff from Costco"
name1 = "Pete Davidson"
name2 = "Shaq O'Neal"
answer_length = 250
provider = 'openai'


persona1, persona2 = generate_debate_personas(debate_topic, name1, name2, provider)

print(f"Persona 1 is: {persona1}")
print(f"Persona 2 is: {persona2}")