import sys, os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
from base import AsyncLLM
from ConversationHandler import ConversationHistory
import asyncio

async def generate_response(llm: AsyncLLM, prompt: str):
    async for chunk in llm(prompt):
        yield chunk

async def run_conversation_test():
    print("Starting 6-turn test for ConversationHistory")

    # Initialize ConversationHistory and LLMs
    summarizer = AsyncLLM("openai", name="summarizer")
    history = ConversationHistory(summarizer)
    
    claude = AsyncLLM("claude", name="claude_1", model="claude-3-5-sonnet-20240620", max_tokens=20)
    gpt = AsyncLLM("openai", name="gpt_1", model="gpt-4o-mini", max_tokens=20)

    # List of prompts for the conversation
    prompts = [
        "What do you think will be the most significant AI advancement in the next decade?",
        "How might quantum computing impact AI and machine learning?",
        "What ethical considerations should we keep in mind with AI advancements?",
        "How can we ensure AI remains beneficial to humanity as it becomes more advanced?",
        "What role should international cooperation play in AI governance?",
        "How can we balance AI innovation with potential risks to society?"
    ]

    current_llm, opponent_llm = claude, gpt

    # Run the conversation
    for turn, prompt in enumerate(prompts):
        print(f"\nTurn {turn + 1}:")
        print(f"Prompt: {prompt}")
        print(f"Response from {current_llm.name}: ", end="", flush=True)

        full_response = ""
        async for chunk in generate_response(current_llm, prompt):
            print(chunk, end="", flush=True)
            full_response += chunk

        print()  # New line after the full response

        await history.add_message(full_response, current_llm.name)

        # Swap current and opponent LLMs
        current_llm, opponent_llm = opponent_llm, current_llm

    # Print the final conversation history
    print("\nFinal conversation history:")
    print(history.get_history())

    # Get and print last messages
    last_messages = history.get_last_messages("claude_1", "gpt_1")

    for llm_name, message in last_messages:
        if message:
            print(f"\nLast message from {llm_name}: {message.content}")
        else:
            print(f"\nNo message found for {llm_name}")

if __name__ == "__main__":
    asyncio.run(run_conversation_test())