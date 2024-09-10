import asyncio
from typing import Tuple, List
from base import AsyncLLM
from ConversationHandler import ConversationHistory
from async_utils import create_persona_llms
from prompts.clash import DEBATE_PROMPT_TEMPLATE

async def generate_response(llm: AsyncLLM, prompt: str):
    async for chunk in llm(prompt):
        yield chunk

async def run_single_turn(current_llm: AsyncLLM, opponent_llm: AsyncLLM, history: ConversationHistory, question: str, turn_count: int, max_words: int = 150):
    last_messages = history.get_last_messages(current_llm.name, opponent_llm.name)
    opponent_last_message = last_messages[1][1].content if last_messages[1][1] else ""
    current_llm_last_msg = last_messages[0][1].content if last_messages[0][1] else ""

    prompt = DEBATE_PROMPT_TEMPLATE.format(
        initial_question=question,
        current_llm_name=current_llm.name,
        opponent_llm_name=opponent_llm.name,
        question_or_continuation=f"Question: {question}" if turn_count == 0 else "Continue the debate based on the previous messages.",
        history=history.get_history(),
        opponent_last_message=opponent_last_message,
        current_llm_last_msg=current_llm_last_msg,
        max_words=max_words,
        address_or_continue="Address the current question with flair" if turn_count == 0 else "Continue the debate based on recent exchanges"
    )

    print(f"\n{'='*50}")
    print(f"Turn {turn_count + 1}: {current_llm.name}'s turn")
    print(f"{'='*50}")
    full_response = ""
    async for chunk in generate_response(current_llm, prompt):
        print(chunk, end="", flush=True)
        full_response += chunk

    await history.add_message(full_response, current_llm.name)
    await history.add_message("<END_TOKEN_WEBSOCKET>", "admin")

    print(f"\n{'='*50}")
    print(f"End of {current_llm.name}'s turn")
    print(f"{'='*50}")
    print("\nWaiting for next turn...")
    await asyncio.sleep(2)  # Simulate 2-second delay between turns

async def run_debate(topic: str, name1: str, name2: str, questions: List[str], num_turns: int = 4):
    print(f"{'*'*50}")
    print(f"Starting debate on: {topic}")
    print(f"Debaters: {name1} vs {name2}")
    print(f"{'*'*50}\n")

    # Generate personas and initialize LLMs
    llm1, llm2 = await create_persona_llms(topic, name1, name2, provider="claude", stream=True, max_tokens=400)
    
    # Initialize ConversationHistory
    summarizer = AsyncLLM("openai", name="summarizer")
    history = ConversationHistory(summarizer)

    current_llm, opponent_llm = llm1, llm2

    for turn_count in range(num_turns):
        question = questions[0] if turn_count == 0 else ""
        
        await run_single_turn(current_llm, opponent_llm, history, question, turn_count)
        
        # Swap current and opponent LLMs
        current_llm, opponent_llm = opponent_llm, current_llm

    print(f"\n{'*'*50}")
    print("Debate concluded!")
    print(f"{'*'*50}")

async def main():
    topic = "The Bulk store whose name is Costco"
    name1 = "Pete Davidson"
    name2 = "Shaq O'Neal"
    questions = [
        "What is the effect of having a lovely trip to Costco every day?",
    ]

    await run_debate(topic, name1, name2, questions, num_turns=6)

if __name__ == "__main__":
    asyncio.run(main())