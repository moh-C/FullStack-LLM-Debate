"""This script demonstrates OpenAI chat completions with an option for streaming."""

import argparse
import os
from dotenv import load_dotenv
from openai import OpenAI


def get_completion(client, stream=False):
    """
    Get chat completion from OpenAI API.

    Args:
        client (OpenAI): The OpenAI client object.
        stream (bool): Whether to stream the response or not.

    Returns:
        str: The completed response.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": (
                    "Tell a 10 line story explaining what 7/11 is! "
                ),
            }
        ],
        stream=stream,
    )

    if stream:
        full_response = ""
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                print(content, end="", flush=True)
                full_response += content
        print("\nDone!\n")
        return full_response
    else:
        return response.choices[0].message.content


def main():
    """Main function to run the OpenAI chat completion example."""
    parser = argparse.ArgumentParser(description="OpenAI Chat Completion Script")
    parser.add_argument(
        "--stream",
        action="store_true",
        help="Enable streaming mode for the response",
    )
    args = parser.parse_args()

    # Load environment variables from .env file
    load_dotenv()

    # Initialize the client
    client = OpenAI()

    # Get and print the completion
    response = get_completion(client, stream=args.stream)

    if not args.stream:
        print(response)
        print("\nDone!\n")


if __name__ == "__main__":
    main()