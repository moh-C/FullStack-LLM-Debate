import sys
import os
import json
import asyncio
from typing import List

# Get the parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

from base import AsyncLLM


async def test_single_call(llm: AsyncLLM, prompt: str) -> None:
    """Test a single call to the AsyncLLM."""
    print(f"\nTesting single call with prompt: {prompt}")
    response = await llm(prompt)
    print(f"Response: {response}")


async def test_multiple_calls(
    llm: AsyncLLM,
    prompts: List[str]
) -> None:
    """Test multiple concurrent calls to the AsyncLLM."""
    print("\nTesting multiple concurrent calls")
    tasks = [llm(prompt) for prompt in prompts]
    responses = await asyncio.gather(*tasks)
    for prompt, response in zip(prompts, responses):
        print(f"Prompt: {prompt}")
        print(f"Response: {response}\n")


async def test_streaming(llm: AsyncLLM, prompt: str) -> None:
    """Test streaming mode of the AsyncLLM."""
    print(f"\nTesting streaming with prompt: {prompt}")
    llm.set_stream(True)
    response = await llm(prompt)
    print(f"\nFull streamed response: {response}")
    llm.set_stream(False)


async def main() -> None:
    """Run all tests for the AsyncLLM class."""
    providers = ["openai", "claude"]

    for provider in providers:
        print(f"\n{'=' * 60}")
        print(f"Testing {provider.upper()} provider")
        print(f"{'=' * 60}")

        print(f"Initializing AsyncLLM with {provider} provider...")
        llm = AsyncLLM(
            provider=provider,
            name=f"Test-{provider}",
            max_tokens=100,
            temperature=0.7
        )
        print("AsyncLLM initialized successfully.")

        print("\n" + "-" * 40)
        print("Test 1: Single API Call")
        print("-" * 40)
        print("This test sends a single prompt to the LLM and awaits the response.")
        await test_single_call(
            llm,
            "What is the capital of France?"
        )

        # print("\n" + "-" * 40)
        # print("Test 2: Multiple Concurrent API Calls")
        # print("-" * 40)
        # print("This test sends multiple prompts concurrently to the LLM and awaits all responses.")
        # prompts = [
        #     "What is the largest planet in our solar system?",
        #     "Who wrote the play 'Romeo and Juliet'?",
        #     "What is the chemical symbol for gold?"
        # ]
        # await test_multiple_calls(llm, prompts)

        # print("\n" + "-" * 40)
        # print("Test 3: Streaming Mode")
        # print("-" * 40)
        # print("This test demonstrates the streaming capability of the AsyncLLM.")
        # print("You should see the response being printed character by character.")
        # await test_streaming(
        #     llm,
        #     "Explain the concept of artificial intelligence in one sentence."
        # )

        # print(f"\nAll tests completed for {provider.upper()} provider.")

    print("\n" + "=" * 60)
    print("All tests for all providers have been completed.")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())