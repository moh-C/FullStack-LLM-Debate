"""Anthropic API script with streaming and non-streaming options."""

import argparse
import os
from dotenv import load_dotenv
from anthropic import Anthropic

# Load environment variables from .env file
load_dotenv()

def get_response(client, stream=False):
    """
    Get response from Anthropic API.

    Args:
        client (Anthropic): The Anthropic client object.
        stream (bool): Whether to stream the response or not.

    Returns:
        str: The completed response.
    """
    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        temperature=0,
        system="You are a world-class poet. Respond only with short poems.",
        messages=[
            {
                "role": "user",
                "content": "Why is the ocean salty?",
            }
        ],
        stream=stream,
    )

    if stream:
        full_response = ""
        for chunk in response:
            if chunk.type == 'content_block_delta':
                if chunk.delta.type == 'text_delta':
                    content = chunk.delta.text
                    print(content, end="", flush=True)
                    full_response += content
        print("\nStreaming completed.")
        return full_response
    else:
        for content in response.content:
            if content.type == 'text':
                return content.text


def main():
    """Main function to run the Anthropic API example."""
    parser = argparse.ArgumentParser(description="Anthropic API Script")
    parser.add_argument(
        "--stream",
        action="store_true",
        help="Enable streaming mode for the response",
    )
    args = parser.parse_args()

    # Retrieve the API key from the environment
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found in environment variables")

    client = Anthropic(api_key=api_key)

    response = get_response(client, stream=args.stream)

    if not args.stream:
        print(response)


if __name__ == "__main__":
    main()