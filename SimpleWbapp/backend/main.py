from fastapi import FastAPI, WebSocket, WebSocketDisconnect
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

openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

client = AsyncOpenAI(api_key=openai_api_key)

async def handle_websocket(websocket: WebSocket, model: str):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            prompt = json.loads(data).get("prompt", "")
            if not prompt:
                await websocket.send_text("Error: No prompt provided")
                continue

            try:
                response = await client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    stream=True
                )
                async for chunk in response:
                    content = chunk.choices[0].delta.content
                    if content:
                        await websocket.send_text(content)
                await websocket.send_text("[DONE]")
            except Exception as e:
                logger.error(f"Error in generating response: {str(e)}")
                await websocket.send_text(f"Error: {str(e)}")
    except WebSocketDisconnect:
        logger.info("WebSocket connection closed")
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")

@app.websocket("/ws1")
async def websocket_endpoint_1(websocket: WebSocket):
    await handle_websocket(websocket, "gpt-4o")

@app.websocket("/ws2")
async def websocket_endpoint_2(websocket: WebSocket):
    await handle_websocket(websocket, "gpt-4o-mini")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)