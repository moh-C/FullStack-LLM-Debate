from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class PersonaInfo(BaseModel):
    name: str
    system_prompt: str

class PersonaResponse(BaseModel):
    persona1: PersonaInfo
    persona2: PersonaInfo

class DebateRequest(BaseModel):
    topic: str
    name1: str
    name2: str
    provider: str = "openai"
    questions: List[str]
    answer_length: int = 150

class DebateTurnSchema(BaseModel):
    turn_number: int
    speaker: str
    content: str
    created_at: datetime

class DebateSchema(BaseModel):
    id: int
    topic: str
    name1: str
    name2: str
    provider: str
    created_at: datetime
    questions: List[str]
    answer_length: int
    turns: List[DebateTurnSchema]

class DebateResponse(BaseModel):
    message: str
    debate_id: int

class OneTurnDebateResponse(BaseModel):
    name: str
    response: str

class DebateHistoryResponse(BaseModel):
    debates: List[DebateSchema]