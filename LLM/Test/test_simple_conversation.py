import sys, os, json

# Get the parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the parent directory to the system path
sys.path.insert(0, parent_dir)
from utils import generate_debate_personas

debate_topic = "Buying bulky stuff from Costco"
name1 = "Pete Davidson"
name2 = "Shaq O'Neal"
provider = "openai"
persona1, persona2 = generate_debate_personas(debate_topic, name1, name2, provider)

print("Persona 1:")
print(json.dumps(persona1, indent=2))
print("\nPersona 2:")
print(json.dumps(persona2, indent=2))