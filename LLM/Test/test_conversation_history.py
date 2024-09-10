import sys, os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
from base import AsyncLLM
from ConversationHandler import ConversationHistory
import asyncio

# Example usage (not part of the class):
async def main():
    summarizer = AsyncLLM("openai", name="summarizer")
    history = ConversationHistory(summarizer)

    # Adding messages
    await history.add_message("Hello, how are you?", "AI_1")
    await history.add_message("I'm doing well, thank you for asking!", "AI_2")
    await history.add_message("That's great to hear!", "AI_1")
    await history.add_message("Indeed, it's always nice to start a conversation on a positive note.", "AI_2")

    # Getting last messages
    current_msg, opponent_msg = history.get_last_messages("AI_1", "AI_2")
    print(f"Last message from AI_1: {current_msg.content if current_msg else 'None'}")
    print(f"Last message from AI_2: {opponent_msg.content if opponent_msg else 'None'}")

    # Printing full history
    print("\nFull conversation history:")
    print(history.get_history())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())