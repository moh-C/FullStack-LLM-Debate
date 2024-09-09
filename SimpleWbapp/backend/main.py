from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
import logging
import asyncio
from openai import AsyncOpenAI

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Predefined prompt
PREDEFINED_PROMPT = "Explain the concept of artificial intelligence in simple terms, providing 5 key points."

async def generate_stream():
    try:
        response = await client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": PREDEFINED_PROMPT}],
            stream=True
        )
        async for chunk in response:
            if chunk.choices[0].delta.content is not None:
                yield f"data: {chunk.choices[0].delta.content}\n\n"
        yield "data: [DONE]\n\n"
    except Exception as e:
        logger.error(f"Error in generate_stream: {str(e)}")
        yield f"data: Error: {str(e)}\n\n"

@app.get("/stream")
async def stream():
    return StreamingResponse(generate_stream(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)