import os
from dotenv import load_dotenv
from openai import OpenAI


def main():
    # Load environment variables from .env file
    load_dotenv()

    # Initialize the client
    client = OpenAI()

    # Create the streaming completion
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": "Tell a 10 line story explaning what 7/11 is! I want it to have at least 1000 words as the output",
            }
        ],
        stream=True,
    )

    # Process the stream
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")


if __name__ == "__main__":
    main()