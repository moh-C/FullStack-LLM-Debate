from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import asyncio

from LLM.base import AsyncLLM
from LLM.ConversationHandler import ConversationHistory
from LLM.async_utils import create_persona_llms
from LLM.prompts.clash import DEBATE_PROMPT_TEMPLATE

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class DebateRequest(BaseModel):
    topic: str
    name1: str
    name2: str
    provider1: str = "gpt-4-0613"
    provider2: str = "gpt-4-0613"
    questions: List[str]

class ContinueRequest(BaseModel):
    num_turns: int = 1

debate_state = {
    "llm1": None,
    "llm2": None,
    "history": None,
    "current_llm": None,
    "opponent_llm": None,
    "turn_count": 0,
    "questions": []
}

async def generate_response(llm: AsyncLLM, prompt: str):
    async for chunk in llm(prompt):
        yield chunk

async def run_single_turn(websocket: WebSocket):
    current_llm = debate_state["current_llm"]
    opponent_llm = debate_state["opponent_llm"]
    history = debate_state["history"]
    turn_count = debate_state["turn_count"]
    question = debate_state["questions"][0] if turn_count == 0 else ""
    max_words = 150

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

    full_response = ""
    async for chunk in generate_response(current_llm, prompt):
        await websocket.send_text(chunk)
        full_response += chunk

    await history.add_message(full_response, current_llm.name)
    await websocket.send_text("<END_TOKEN_WEBSOCKET>")

    debate_state["current_llm"], debate_state["opponent_llm"] = debate_state["opponent_llm"], debate_state["current_llm"]
    debate_state["turn_count"] += 1

@app.post("/start_debate")
async def start_debate(request: DebateRequest):
    debate_state["llm1"], debate_state["llm2"] = await create_persona_llms(
        request.topic,
        request.name1,
        request.name2,
        provider=request.provider1,
        stream=True,
        max_tokens=400
    )
    
    summarizer = AsyncLLM("openai", name="summarizer")
    debate_state["history"] = ConversationHistory(summarizer)
    debate_state["current_llm"], debate_state["opponent_llm"] = debate_state["llm1"], debate_state["llm2"]
    debate_state["turn_count"] = 0
    debate_state["questions"] = request.questions

    return {"message": "Debate initialized. Connect to WebSocket to start."}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            await run_single_turn(websocket)
            await websocket.receive_text()  # Wait for a message from the client to continue
    except WebSocketDisconnect:
        print("WebSocket disconnected")

@app.post("/continue")
async def continue_debate(request: ContinueRequest):
    return {"message": f"Use WebSocket to continue for {request.num_turns} turns"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)