import os, re
import json
from typing import Tuple, Dict, Literal, List
from LLM.base import AsyncLLM
from LLM.prompts.Persona import SET_PERSONA
from app.models import Persona
from sqlalchemy.orm import Session


async def generate_debate_personas(
    debate_topic: str,
    name1: str,
    name2: str,
    persona_db: Session,
    answer_length: int = 400,
    provider: Literal["openai", "claude"] = "openai",
) -> Tuple[Dict[str, str], Dict[str, str]]:
    # Ensure name1 and name2 are always in the same order
    sorted_names = sorted([name1, name2])
    name1, name2 = sorted_names

    # Check if personas exist in the database
    existing_persona = persona_db.query(Persona).filter(
        Persona.topic == debate_topic,
        Persona.name1 == name1,
        Persona.name2 == name2,
        Persona.answer_length == answer_length,
        Persona.provider == provider
    ).first()

    if existing_persona:
        return (
            {"name": existing_persona.persona1_name, "system_prompt": existing_persona.persona1_system_prompt},
            {"name": existing_persona.persona2_name, "system_prompt": existing_persona.persona2_system_prompt}
        )

    # Generate new personas
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
    
    personas = extract_persona_data(response)

    if len(personas) != 2:
        raise ValueError(f"Expected 2 personas, but got {len(personas)}")

    # Save new personas to the database
    new_persona = Persona(
        topic=debate_topic,
        name1=name1,
        name2=name2,
        persona1_name=personas[0]["name"],
        persona2_name=personas[1]["name"],
        persona1_system_prompt=personas[0]["system_prompt"],
        persona2_system_prompt=personas[1]["system_prompt"],
        answer_length=answer_length,
        provider=provider
    )
    persona_db.add(new_persona)
    persona_db.commit()

    return tuple(
        {
            "name": persona["name"],
            "system_prompt": persona["system_prompt"]
        }
        for persona in personas
    )

def extract_persona_data(xml_string: str) -> List[Dict[str, str]]:
    """
    Extract persona data from an XML string.

    Args:
        xml_string (str): XML string containing persona data.

    Returns:
        List[Dict[str, str]]: List of dictionaries containing persona data.
    """
    personas = []
    persona_pattern = r'<persona>\s*<name>(.*?)</name>\s*<systemprompt>(.*?)</systemprompt>\s*</persona>'
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
    temperature: float = 0.7,
    persona_db: Session = None
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
    personas = await generate_debate_personas(
        debate_topic,
        name1,
        name2,
        provider=provider,
        persona_db=persona_db
        )

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