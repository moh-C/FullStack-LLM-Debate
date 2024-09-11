from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from app.database import get_debate_db, get_persona_db
from .debate import debate_state, generate_debate_response
import logging

router = APIRouter()

logger = logging.getLogger(__name__)

@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket, 
    debate_db: Session = Depends(get_debate_db),
    persona_db: Session = Depends(get_persona_db)
):
    await websocket.accept()
    try:
        while True:
            # Wait for a signal from the client to generate the next turn
            await websocket.receive_text()
            
            async for response_chunk in generate_debate_response(debate_db, persona_db):
                await websocket.send_json(response_chunk)
            await websocket.send_text("<END_WEBSOCKET_TOKEN>")
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")