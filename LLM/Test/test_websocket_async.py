import sys, os
import asyncio
from typing import List

# Get the parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

import asyncio
import websockets
from base import AsyncLLM

async def llm_handler(websocket, path):
    llm = AsyncLLM(provider="openai", stream=True)  # You can change the provider if needed
    
    async for message in websocket:
        print(f"Received message: {message}")
        
        async for chunk in llm(message):
            await websocket.send(chunk)

async def start_server():
    server = await websockets.serve(llm_handler, "localhost", 8765)
    await server.wait_closed()

async def test_client():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        test_message = "Tell me a short story about a robot."
        await websocket.send(test_message)
        print(f"Sent message: {test_message}")
        
        full_response = ""
        try:
            while True:
                try:
                    message = await asyncio.wait_for(websocket.recv(), timeout=2.0)
                    print(f"Received chunk: {message}")
                    full_response += message
                except asyncio.TimeoutError:
                    print("No more data received for 2 seconds. Assuming end of stream.")
                    break
        except websockets.exceptions.ConnectionClosed:
            print("WebSocket connection closed")
        
        print(f"Full response:\n{full_response}")

async def main():
    server_task = asyncio.create_task(start_server())
    await asyncio.sleep(1)  # Give the server time to start
    
    await test_client()
    
    server_task.cancel()
    try:
        await server_task
    except asyncio.CancelledError:
        pass

if __name__ == "__main__":
    asyncio.run(main())