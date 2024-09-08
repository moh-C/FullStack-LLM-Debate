import re

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