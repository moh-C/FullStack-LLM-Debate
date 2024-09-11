from app.models import Debate, DebateTurn
from LLM.prompts.clash import DEBATE_PROMPT_TEMPLATE
from app.schemas import (
    DebateRequest, DebateResponse, DebateSchema, OneTurnDebateResponse,
    PersonaResponse, DebateHistoryResponse, DebateHistoryItem, TurnSchema
)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.database import get_debate_db, get_persona_db
from app.schemas import DebateRequest, DebateResponse
from app.models import Debate
from LLM.base import AsyncLLM
from LLM.ConversationHandler import ConversationHistory
from LLM.async_utils import generate_debate_personas
import json
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

debate_state = {
    "llm1": None,
    "llm2": None,
    "history": None,
    "current_llm": None,
    "opponent_llm": None,
    "turn_count": 0,
    "questions": [],
    "personas": None,
    "answer_length": 100,
    "current_debate_id": None
}

def generate_prompt():
    current_llm = debate_state["current_llm"]
    opponent_llm = debate_state["opponent_llm"]
    history = debate_state["history"]
    turn_count = debate_state["turn_count"]
    question = debate_state["questions"][0] if turn_count == 0 else ""
    max_words = debate_state["answer_length"]

    last_messages = history.get_last_messages(current_llm.name, opponent_llm.name)
    opponent_last_message = last_messages[1][1].content if last_messages[1][1] else ""
    current_llm_last_msg = last_messages[0][1].content if last_messages[0][1] else ""

    return DEBATE_PROMPT_TEMPLATE.format(
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

async def generate_debate_response(debate_db: Session, persona_db: Session):
    current_llm = debate_state["current_llm"]
    prompt = generate_prompt()

    full_response = ""
    async for chunk in current_llm(prompt):
        full_response += chunk
        yield {"name": current_llm.name, "chunk": chunk}

    await debate_state["history"].add_message(full_response, current_llm.name)

    new_turn = DebateTurn(
        debate_id=debate_state["current_debate_id"],
        speaker=current_llm.name,
        content=full_response,
        prompt=prompt,
        turn_number=debate_state["turn_count"]
    )
    debate_db.add(new_turn)
    debate_db.commit()

    debate_state["current_llm"], debate_state["opponent_llm"] = debate_state["opponent_llm"], debate_state["current_llm"]
    debate_state["turn_count"] += 1


@router.post("/start_debate", response_model=DebateResponse)
async def start_debate(request: DebateRequest):
    logger.info(f"Received start_debate request: {request}")
    
    # Initialize database sessions
    debate_db = next(get_debate_db())
    persona_db = next(get_persona_db())
    
    try:
        logger.debug("About to call generate_debate_personas")
        logger.debug(f"Arguments: debate_topic={request.topic}, name1={request.name1}, name2={request.name2}, persona_db={persona_db}, answer_length={request.answer_length}, provider={request.provider}")
        
        debate_state["personas"] = await generate_debate_personas(
            debate_topic=request.topic,
            name1=request.name1,
            name2=request.name2,
            persona_db=persona_db,
            answer_length=request.answer_length,
            provider=request.provider
        )
        
        logger.debug("generate_debate_personas completed successfully")
        
        # Create LLMs using the generated personas
        debate_state["llm1"] = AsyncLLM(
            provider=request.provider,
            name=debate_state["personas"][0]["name"],
            stream=True,
            max_tokens=request.answer_length * 3,
            temperature=0.7,
            system_prompt=debate_state["personas"][0]["system_prompt"]
        )

        debate_state["llm2"] = AsyncLLM(
            provider=request.provider,
            name=debate_state["personas"][1]["name"],
            stream=True,
            max_tokens=request.answer_length * 3,
            temperature=0.7,
            system_prompt=debate_state["personas"][1]["system_prompt"]
        )
        
        summarizer = AsyncLLM(request.provider, name="summarizer")
        debate_state["history"] = ConversationHistory(summarizer)
        
        debate_state["current_llm"], debate_state["opponent_llm"] = debate_state["llm1"], debate_state["llm2"]
        debate_state["turn_count"] = 0
        debate_state["questions"] = request.questions
        debate_state["answer_length"] = request.answer_length

        new_debate = Debate(
            topic=request.topic,
            name1=request.name1,
            name2=request.name2,
            provider=request.provider,
            questions=json.dumps(request.questions),
            answer_length=request.answer_length,
            persona1=json.dumps({
                "name": debate_state["personas"][0]["name"],
                "system_prompt": debate_state["personas"][0]["system_prompt"]
            }),
            persona2=json.dumps({
                "name": debate_state["personas"][1]["name"],
                "system_prompt": debate_state["personas"][1]["system_prompt"]
            })
        )
        debate_db.add(new_debate)
        debate_db.commit()
        debate_db.refresh(new_debate)
        
        debate_state["current_debate_id"] = new_debate.id

        return DebateResponse(message="Debate initialized. Connect to WebSocket or use /one_turn_debate to progress.", debate_id=new_debate.id)
    except Exception as e:
        logger.error(f"Error in start_debate: {str(e)}")
        logger.exception("Full exception traceback:")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Close database sessions
        debate_db.close()
        persona_db.close()
    

@router.post("/one_turn_debate", response_model=OneTurnDebateResponse)
async def one_turn_debate(
    debate_db: Session = Depends(get_debate_db),
    persona_db: Session = Depends(get_persona_db)
):
    logger.info("Received request for one_turn_debate")
    
    if not debate_state["current_llm"]:
        logger.error("Debate not initialized")
        raise HTTPException(status_code=400, detail="Debate not initialized. Call /start_debate first.")

    current_llm = debate_state["current_llm"]
    turn_count = debate_state["turn_count"]

    logger.info(f"Current turn count: {turn_count}")
    logger.info(f"Current speaker: {current_llm.name}")

    prompt = generate_prompt()
    logger.info(f"Generated prompt: {prompt}")

    full_response = ""
    async for chunk in current_llm(prompt):
        full_response += chunk

    logger.info(f"Generated response: {full_response}")

    await debate_state["history"].add_message(full_response, current_llm.name)

    new_turn = DebateTurn(
        debate_id=debate_state["current_debate_id"],
        speaker=current_llm.name,
        content=full_response,
        prompt=prompt,
        turn_number=turn_count
    )
    debate_db.add(new_turn)
    debate_db.commit()

    logger.info(f"Saved turn to database: turn_number={turn_count}, speaker={current_llm.name}")

    debate_state["current_llm"], debate_state["opponent_llm"] = debate_state["opponent_llm"], debate_state["current_llm"]
    debate_state["turn_count"] += 1

    logger.info(f"Updated debate state: turn_count={debate_state['turn_count']}, next_speaker={debate_state['current_llm'].name}")

    return OneTurnDebateResponse(name=current_llm.name, response=full_response)

@router.get("/debate/{debate_id}", response_model=DebateSchema)
async def get_debate(debate_id: int, db: Session = Depends(get_debate_db)):
    debate = db.query(Debate).filter(Debate.id == debate_id).first()
    if debate is None:
        raise HTTPException(status_code=404, detail="Debate not found")
    
    turns = db.query(DebateTurn).filter(DebateTurn.debate_id == debate_id).order_by(DebateTurn.turn_number).all()
    
    return DebateSchema(
        id=debate.id,
        topic=debate.topic,
        name1=debate.name1,
        name2=debate.name2,
        provider=debate.provider,
        created_at=debate.created_at,
        questions=json.loads(debate.questions),
        answer_length=debate.answer_length,
        turns=[
            {
                "turn_number": turn.turn_number,
                "speaker": turn.speaker,
                "content": turn.content,
                "prompt": turn.prompt,
                "created_at": turn.created_at
            }
            for turn in turns
        ]
    )

@router.get("/debate_history", response_model=DebateHistoryResponse)
async def get_debate_history(limit: int = 10, db: Session = Depends(get_debate_db)):
    debates = db.query(Debate).order_by(desc(Debate.created_at)).limit(limit).all()
    return DebateHistoryResponse(
        debates=[
            {
                "id": debate.id,
                "topic": debate.topic,
                "name1": debate.name1,
                "name2": debate.name2,
                "provider": debate.provider,
                "created_at": debate.created_at,
                "questions": json.loads(debate.questions),
                "answer_length": debate.answer_length,
                "persona1": json.loads(debate.persona1) if debate.persona1 else None,
                "persona2": json.loads(debate.persona2) if debate.persona2 else None
            }
            for debate in debates
        ]
    )