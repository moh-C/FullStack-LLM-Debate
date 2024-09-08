SET_PERSONA = """
Generate two opposing AI debater personas with their respective user and system prompts based on the following:
Conversation topic: {debate_topic}
Persona 1 name: {name1}
Persona 2 name: {name2}

For each persona, create:
1. A user prompt (2-3 sentences) that:
   * Introduces the persona
   * Sets the debate topic
   * Encourages funny and opposing behavior

A system prompt (5-7 bullet points) that:
- Defines the persona's unique traits and speech patterns
- Instructs how to approach the debate humorously
- Encourages opposition to the other persona
- Provides guidelines for entertaining responses
- Ensure both personas are funny, opposing each other, and thrilling to watch/read.
- Should include that the output for that conversation should NOT be more than {answer_length} words!

Important: Make you entire output is in xml format, nothing extra! so no explanations!

Example output format:
<personas>
<persona>
<name></name>
<userprompt>
</userprompt>
<systemprompt></systemprompt>
</persona>

<persona>
<name></name>
<userprompt>
</userprompt>
<systemprompt></systemprompt>
</persona>
</personas>
"""