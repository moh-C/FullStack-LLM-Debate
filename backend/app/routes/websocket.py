from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from .debate import debate_state, generate_debate_response
import logging

router = APIRouter()

logger = logging.getLogger(__name__)

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):
    await websocket.accept()
    try:
        while True:
            # Wait for a signal from the client to generate the next turn
            await websocket.receive_text()
            
            async for response_chunk in generate_debate_response(db):
                await websocket.send_json(response_chunk)
            await websocket.send_text("<END_WEBSOCKET_TOKEN>")
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")