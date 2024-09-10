import traceback
import logging
from typing import List, Optional
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from LLM.base import AsyncLLM
from LLM.ConversationHandler import ConversationHistory
from LLM.async_utils import create_persona_llms, generate_debate_personas
from LLM.prompts.clash import DEBATE_PROMPT_TEMPLATE

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Debugging middleware
@app.middleware("http")
async def debug_middleware(request: Request, call_next):
    logger.info(f"Received {request.method} request to {request.url}")
    try:
        response = await call_next(request)
        logger.info(f"Responding with status code {response.status_code}")
        return response
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        logger.error(traceback.format_exc())
        return JSONResponse(status_code=500, content={"detail": str(e)})

class DebateRequest(BaseModel):
    topic: str
    name1: str
    name2: str
    provider1: str = "gpt-4-0613"
    provider2: str = "gpt-4-0613"
    questions: List[str]
    answer_length: int = 400

debate_state = {
    "llm1": None,
    "llm2": None,
    "history": None,
    "current_llm": None,
    "opponent_llm": None,
    "turn_count": 0,
    "questions": [],
    "personas": None
}

@app.options("/{full_path:path}")
async def options_route(request: Request):
    return JSONResponse(
        content="OK",
        headers={
            "Access-Control-Allow-Origin": "http://localhost:3000",
            "Access-Control-Allow-Methods": "POST, GET, DELETE, PUT, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
        },
    )

@app.get("/")
async def root():
    return {"message": "Welcome to the Debate API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/start_debate")
async def start_debate(request: DebateRequest):
    logger.info(f"Received start_debate request: {request}")
    try:
        debate_state["personas"] = await generate_debate_personas(
            request.topic,
            request.name1,
            request.name2,
            answer_length=400,
            provider="openai"
        )
        
        debate_state["llm1"], debate_state["llm2"] = await create_persona_llms(
            request.topic,
            request.name1,
            request.name2,
            provider="openai",
            stream=True,
            max_tokens=400
        )
        
        summarizer = AsyncLLM("openai", name="summarizer")
        debate_state["history"] = ConversationHistory(summarizer)
        debate_state["current_llm"], debate_state["opponent_llm"] = debate_state["llm1"], debate_state["llm2"]
        debate_state["turn_count"] = 0
        debate_state["questions"] = request.questions

        return {"message": "Debate initialized. Connect to WebSocket to start."}
    except Exception as e:
        logger.error(f"Error in start_debate: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            await run_single_turn(websocket)
            await websocket.receive_text()  # Wait for a message from the client to continue
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")

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

async def generate_response(llm: AsyncLLM, prompt: str):
    async for chunk in llm(prompt):
        yield chunk

@app.get("/persona")
async def get_persona():
    if debate_state["personas"] is None:
        return {"error": "Personas not yet generated. Start a debate first."}
    return {
        "persona1": {
            "name": debate_state["personas"][0]["name"],
            "system_prompt": debate_state["personas"][0]["system_prompt"]
        },
        "persona2": {
            "name": debate_state["personas"][1]["name"],
            "system_prompt": debate_state["personas"][1]["system_prompt"]
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)