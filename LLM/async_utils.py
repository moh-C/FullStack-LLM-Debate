import os, re
import json
from typing import Tuple, Dict, Literal, List
from base import AsyncLLM
from prompts.Persona import SET_PERSONA

CACHE_DIR = "cache"

async def generate_debate_personas(
    debate_topic: str,
    name1: str,
    name2: str,
    answer_length: int = 400,
    provider: Literal["openai", "claude"] = "openai"
) -> Tuple[Dict[str, str], Dict[str, str]]:
    """
    Generate debate personas based on the given topic and names asynchronously.

    Args:
        debate_topic (str): The topic of the debate.
        name1 (str): Name of the first debater.
        name2 (str): Name of the second debater.
        answer_length (int): Length of the debate per turn.
        provider (Literal["openai", "claude"]): The LLM provider to use.

    Returns:
        Tuple[Dict[str, str], Dict[str, str]]: Two dictionaries containing
        the name, user prompt, and system prompt for each persona.
    """
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_key = f"{debate_topic}_{name1}_{name2}_{provider}".replace(" ", "_")
    cache_file = os.path.join(CACHE_DIR, f"{cache_key}.json")

    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            return tuple(json.load(f))

    prompt = SET_PERSONA.format(
        debate_topic=debate_topic,
        name1=name1,
        name2=name2,
        answer_length=answer_length
    )

    llm = AsyncLLM(provider=provider, stream=False)
    response = ""
    async for chunk in llm(user_prompt=prompt):
        response += chunk
    print(f"response is: {response}")
    personas = extract_persona_data(response)

    if len(personas) != 2:
        raise ValueError(f"Expected 2 personas, but got {len(personas)}")

    result = tuple(
        {
            "name": persona["name"],
            "system_prompt": persona["system_prompt"]
        }
        for persona in personas
    )

    with open(cache_file, 'w') as f:
        json.dump(result, f)

    return result


def extract_persona_data(xml_string: str) -> List[Dict[str, str]]:
    """
    Extract persona data from an XML string, including CDATA content.

    Args:
        xml_string (str): XML string containing persona data.

    Returns:
        List[Dict[str, str]]: List of dictionaries containing persona data.
    """
    personas = []
    persona_pattern = r'<persona>\s*<name>(.*?)</name>\s*<systemprompt>\s*<!\[CDATA\[(.*?)\]\]>\s*</systemprompt>\s*</persona>'
    matches = re.findall(persona_pattern, xml_string, re.DOTALL)
    
    for match in matches:
        name, system_prompt = match
        # Preserve formatting but remove leading/trailing whitespace
        system_prompt = "\n".join(line.strip() for line in system_prompt.split('\n') if line.strip())
        
        personas.append({
            'name': name.strip(),
            'system_prompt': system_prompt
        })
    
    return personas


async def create_persona_llms(
    debate_topic: str,
    name1: str,
    name2: str,
    provider: Literal["openai", "claude"] = "openai",
    stream: bool = True,
    max_tokens: int = 400,
    temperature: float = 0.7
) -> Tuple[AsyncLLM, AsyncLLM]:
    """
    Create LLM objects for two debate personas asynchronously.

    Args:
        debate_topic (str): The topic of the debate.
        name1 (str): Name of the first debater.
        name2 (str): Name of the second debater.
        provider (Literal["openai", "claude"]): The LLM provider to use.
        stream (bool): Whether to enable streaming for the LLMs.
        max_tokens (int): Maximum number of tokens for LLM responses.
        temperature (float): Temperature setting for the LLMs.

    Returns:
        Tuple[LLM, LLM]: Two LLM objects, one for each persona.
    """
    personas = await generate_debate_personas(debate_topic, name1, name2, provider=provider)

    llm1 = AsyncLLM(
        provider=provider,
        name=personas[0]["name"],
        stream=stream,
        max_tokens=max_tokens,
        temperature=temperature,
        system_prompt=personas[0]["system_prompt"]
    )

    llm2 = AsyncLLM(
        provider=provider,
        name=personas[1]["name"],
        stream=stream,
        max_tokens=max_tokens,
        temperature=temperature,
        system_prompt=personas[1]["system_prompt"]
    )

    return llm1, llm2