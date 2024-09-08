from base import LLM

# For OpenAI
llm1 = LLM(provider="openai", stream=False)
response1 = llm1("What is your take on Python?")
print(response1)

# For Claude
llm2 = LLM(provider="claude", stream=False)
response2 = llm2("What is your take on Python?")
print(response2)