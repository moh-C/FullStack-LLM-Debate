import asyncio
import websockets
import aiohttp
import json
import os

# Get the host IP from environment variable or use a default
HOST_IP = os.environ.get('HOST_IP', '172.17.0.1')  # Default Docker host IP

async def check_server(session, base_url):
    try:
        async with session.get(f"{base_url}/") as response:
            if response.status == 200:
                print("Server is running.")
            else:
                print(f"Server returned unexpected status: {response.status}")
    except Exception as e:
        print(f"Error checking server: {e}")

async def check_health(session, base_url):
    try:
        async with session.get(f"{base_url}/health") as response:
            if response.status == 200:
                print("Server health check passed.")
            else:
                print(f"Health check failed with status: {response.status}")
    except Exception as e:
        print(f"Error checking server health: {e}")

async def start_debate(session, base_url, debate_topic, name1, name2, answer_length, provider1, provider2):
    url = f"{base_url}/start_debate"
    data = {
        "topic": debate_topic,
        "name1": name1,
        "name2": name2,
        "provider1": provider1,
        "provider2": provider2,
        "questions": ["What are your thoughts on this topic?"],
        "answer_length": answer_length
    }
    print("Waiting 2 seconds before making the request...")
    await asyncio.sleep(2)  # Wait for 2 seconds before making the request
    try:
        async with session.post(url, json=data) as response:
            result = await response.json()
            print(result)
    except Exception as e:
        print(f"An error occurred while starting the debate: {e}")
        raise

# ... (get_persona and debate_websocket functions remain the same)

async def main():
    base_url = f"http://{HOST_IP}:8000"
    ws_url = f"ws://{HOST_IP}:8000/ws"
    
    print(f"Using HOST_IP: {HOST_IP}")
    
    debate_topic = "Buying tons of stuff from Costco!"
    name1 = "Pete Davidson"
    name2 = "Shaq O'Neal"
    answer_length = 150
    provider1 = "claude"
    provider2 = "claude"

    async with aiohttp.ClientSession() as session:
        await check_server(session, base_url)
        await check_health(session, base_url)
        await start_debate(session, base_url, debate_topic, name1, name2, answer_length, provider1, provider2)
        await get_persona(session, base_url)
    
    await debate_websocket(ws_url)

if __name__ == "__main__":
    asyncio.run(main())