import time
import tiktoken
from typing import List
from base import LLM  # Assuming the LLM class is in a file named base.py

# Initialize the tokenizer
enc = tiktoken.encoding_for_model("gpt-3.5-turbo")

def count_tokens(text: str) -> int:
    return len(enc.encode(text))

def count_words(text: str) -> int:
    return len(text.split())

def summarize_context(context: List[str], llm: LLM, max_tokens: int = 500) -> str:
    context_text = "\n".join(context)
    prompt = f"Summarize the following conversation in about {max_tokens//2} tokens and no more than 100 words:\n\n{context_text}\n\nSummary:"
    summary = llm(prompt)
    return f"Summary of previous conversation: {summary}"

def llm_chat(num_turns: int = 5, max_context_tokens: int = 1000):
    context = []
    
    # Initialize LLM instances
    claude_llm = LLM(provider="claude", stream=False, temperature=0.7, max_tokens=200)  # Increased max_tokens to allow for full 100 words
    openai_llm = LLM(provider="openai", stream=False, temperature=0.7, max_tokens=200)
    
    personas = {
        "Claude": "You are a curious scientist always eager to learn new things. Respond in no more than 100 words.",
        "OpenAI": "You are a wise philosopher who enjoys deep, thoughtful discussions. Respond in no more than 100 words.",
        "AI_Moderator": "You are an AI assistant helping to moderate the conversation. Your role is to guide the discussion, ask probing questions, and ensure both Claude and OpenAI stay on topic. Occasionally summarize key points. Respond in no more than 100 words."
    }
    
    # Initial prompt to start the conversation
    initial_topic = input("Enter the initial topic for discussion: ")
    context.append(f"Human_Moderator: Let's begin a discussion on {initial_topic}. Claude, as our curious scientist, would you like to start? Remember, all responses should be no more than 100 words.")
    
    for i in range(num_turns):
        for role in ["Claude", "OpenAI", "Moderator"]:
            # Check if context needs summarization
            context_tokens = count_tokens("\n".join(context))
            if context_tokens > max_context_tokens:
                summary = summarize_context(context, claude_llm)
                context = [summary]
                print(f"Context summarized. New token count: {count_tokens(summary)}")
            
            if role == "Moderator":
                human_input = input("Your turn as moderator (press Enter to let AI moderate): ").strip()
                if human_input:
                    context.append(f"Human_Moderator: {human_input}")
                    print(f"Human_Moderator: {human_input}")
                    continue
                else:
                    role = "AI_Moderator"
            
            # Construct the prompt
            prompt = f"{personas[role]}\n\nHere's the conversation so far:\n"
            prompt += "\n".join(context[-5:])  # Only include the last 5 turns to save context space
            prompt += f"\n\n{role} (remember to respond in no more than 100 words): "
            
            # Get response from LLM
            if role == "Claude":
                response = claude_llm(prompt)
            elif role == "OpenAI":
                response = openai_llm(prompt)
            else:  # AI_Moderator
                response = claude_llm(prompt)  # Using Claude for moderation, but you can change this if preferred
            
            if response:
                # Truncate response to 100 words if it exceeds the limit
                words = response.split()
                if len(words) > 100:
                    response = " ".join(words[:100]) + "..."
                
                context.append(f"{role}: {response}")
                print(f"{role}: {response}")
                print(f"Word count: {count_words(response)}")
            else:
                print(f"Failed to get response for {role}")
            
            time.sleep(1)  # To avoid hitting API rate limits

    return context

# Run the chat
conversation = llm_chat()

# Print the full conversation
print("\nFull conversation:")
for turn in conversation:
    print(turn)