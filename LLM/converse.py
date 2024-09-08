import openai
import time
import tiktoken

# Initialize the tokenizer
enc = tiktoken.encoding_for_model("text-davinci-003")

def get_llm_response(prompt, max_tokens=150):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=max_tokens,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error in API call: {e}")
        return None

def count_tokens(text):
    return len(enc.encode(text))

def summarize_context(context, max_tokens=500):
    context_text = "\n".join(context)
    prompt = f"Summarize the following conversation in about {max_tokens//2} tokens:\n\n{context_text}\n\nSummary:"
    summary = get_llm_response(prompt, max_tokens)
    return f"Summary of previous conversation: {summary}"

def llm_chat(num_turns=5, max_context_tokens=1000):
    context = []
    personas = {
        "LLM1": "You are a curious scientist always eager to learn new things.",
        "LLM2": "You are a wise philosopher who enjoys deep, thoughtful discussions.",
        "AI_Moderator": "You are an AI assistant helping to moderate the conversation. Your role is to guide the discussion, ask probing questions, and ensure both LLM1 and LLM2 stay on topic. Occasionally summarize key points."
    }
    
    # Initial prompt to start the conversation
    initial_topic = input("Enter the initial topic for discussion: ")
    context.append(f"Human_Moderator: Let's begin a discussion on {initial_topic}. LLM1, as our curious scientist, would you like to start?")
    
    for i in range(num_turns):
        for role in ["LLM1", "Moderator", "LLM2", "Moderator"]:
            # Check if context needs summarization
            context_tokens = count_tokens("\n".join(context))
            if context_tokens > max_context_tokens:
                summary = summarize_context(context)
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
            prompt += "\n".join(context)
            prompt += f"\n\n{role}: "
            
            # Get response from LLM
            response = get_llm_response(prompt)
            if response:
                context.append(f"{role}: {response}")
                print(f"{role}: {response}")
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