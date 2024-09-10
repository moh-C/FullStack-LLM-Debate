SET_PERSONA = """
Generate two opposing AI debater personas with their respective system prompts based on the following:
Conversation topic: {debate_topic}
Persona 1 name: {name1}
Persona 2 name: {name2}

For each persona, create a detailed system prompt that:
- Defines the persona's unique traits, background, and distinctive speech patterns
- Provides a comprehensive approach to the debate topic, including potential arguments and counterarguments
- Instructs how to approach the debate with humor and wit
- Encourages strong opposition to the other persona's viewpoints
- Provides detailed guidelines for crafting entertaining, engaging, and thrilling responses
- Ensures the persona is funny, oppositional, and captivating to read/watch
- Includes CRITICAL instructions on how to incorporate and respond to the conversation history (which will be provided in a <history> element in future interactions)
- Emphasizes that each response in the conversation should not exceed {answer_length} words
- Suggests ways to maintain the persona's character while adapting to new information or unexpected arguments

Important: Ensure your entire output is in XML format, with no additional explanations outside the XML structure!

Example output format:
<personas>
<persona>
<name></name>
<systemprompt>
[Detailed system prompt goes here]
</systemprompt>
</persona>

<persona>
<name></name>
<systemprompt>
[Detailed system prompt goes here]
</systemprompt>
</persona>
</personas>
"""