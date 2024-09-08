import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Initialize the client
client = OpenAI()

# Create the streaming completion
stream = client.chat.completions.create(
    model="gpt-4",  # Make sure this is a valid model name
    messages=[{"role": "user", "content": "Say this is a test"}],
    stream=True,
)

# Process the stream
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")