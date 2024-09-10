import logging
from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
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

        return {"message": "Debate initialized. Connect to WebSocket or use /one_turn_debate to progress."}
    except Exception as e:
        logger.error(f"Error in start_debate: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def generate_debate_response():
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
    async for chunk in current_llm(prompt):
        full_response += chunk
        yield {"name": current_llm.name, "chunk": chunk}

    await history.add_message(full_response, current_llm.name)

    debate_state["current_llm"], debate_state["opponent_llm"] = debate_state["opponent_llm"], debate_state["current_llm"]
    debate_state["turn_count"] += 1

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Wait for a signal from the client to generate the next turn
            await websocket.receive_text()
            
            async for response_chunk in generate_debate_response():
                await websocket.send_json(response_chunk)
            await websocket.send_text("<END_WEBSOCKET_TOKEN>")
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")

@app.post("/one_turn_debate")
async def one_turn_debate():
    if not debate_state["current_llm"]:
        raise HTTPException(status_code=400, detail="Debate not initialized. Call /start_debate first.")

    full_response = ""
    current_name = debate_state["current_llm"].name
    async for response_chunk in generate_debate_response():
        full_response += response_chunk["chunk"]
    
    return {"name": current_name, "response": full_response}

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