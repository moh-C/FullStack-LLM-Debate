import sys, os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
from base import AsyncLLM
from ConversationHandler import ConversationHistory
import asyncio

async def get_llm_response(name: str, prompt: str) -> str:
    if name == "claude_1":
        llm = AsyncLLM("claude", name="claude_1", model="claude-3-5-sonnet-20240620", max_tokens=20)
    elif name == "gpt_1":
        llm = AsyncLLM("openai", name="gpt_1", model="gpt-4o-mini", max_tokens=20)
    else:
        raise ValueError(f"Unknown LLM name: {name}")

    full_response = ""
    async for chunk in llm(prompt):
        full_response += chunk
    
    return full_response

async def run_six_turn_test():
    print("Starting 6-turn test for ConversationHistory")

    # Initialize ConversationHistory
    summarizer = AsyncLLM("openai", name="summarizer")
    history = ConversationHistory(summarizer)

    # 6-turn conversation between Claude and GPT
    turns = [
        ("claude_1", "Let's discuss the future of AI. What do you think will be the most significant advancement in the next decade?"),
        ("gpt_1", "Interesting question. I believe quantum computing integration with AI could be revolutionary. What's your perspective on this?"),
        ("claude_1", "Quantum computing in AI is fascinating. How do you think it might impact machine learning algorithms and model training?"),
        ("gpt_1", "Quantum computing could dramatically speed up complex calculations in ML. What ethical considerations should we keep in mind with such advancements?"),
        ("claude_1", "Ethical considerations are crucial. How can we ensure AI remains beneficial to humanity as it becomes more advanced?"),
        ("gpt_1", "Ensuring beneficial AI is a complex challenge. What role do you think international cooperation should play in AI governance?")
    ]

    # Add messages to the conversation history
    for sender, content in turns:
        response = await get_llm_response(sender, content)
        await history.add_message(response, sender)
        print(f"Turn by {sender}:")
        print(f"  Prompt: {content}")
        print(f"  Response: {response}")
        print()

    # Print the final conversation history
    print("Final conversation history:")
    print(history.get_history())

    # In your test script
    last_messages = history.get_last_messages("claude_1", "gpt_1")

    for llm_name, message in last_messages:
        if message:
            print(f"Last message from {llm_name}: {message.content}")
        else:
            print(f"No message found for {llm_name}")

if __name__ == "__main__":
    asyncio.run(run_six_turn_test())