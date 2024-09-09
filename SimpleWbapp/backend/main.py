from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
import logging
import json
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

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            prompt = json.loads(data)["prompt"]
            
            try:
                response = await client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    stream=True
                )
                async for chunk in response:
                    if chunk.choices[0].delta.content is not None:
                        await websocket.send_text(chunk.choices[0].delta.content)
                await websocket.send_text("[DONE]")
            except Exception as e:
                logger.error(f"Error in generate_stream: {str(e)}")
                await websocket.send_text(f"Error: {str(e)}")
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)