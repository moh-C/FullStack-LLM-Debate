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

class TurnSchema(BaseModel):
    turn_number: int
    speaker: str
    content: str
    prompt: str
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
    turns: List[TurnSchema]

class DebateResponse(BaseModel):
    message: str
    debate_id: int

class OneTurnDebateResponse(BaseModel):
    name: str
    response: str

class DebateHistoryItem(BaseModel):
    id: int
    topic: str
    name1: str
    name2: str
    provider: str
    created_at: datetime
    questions: List[str]
    answer_length: int
    persona1: Optional[dict]
    persona2: Optional[dict]

class DebateHistoryResponse(BaseModel):
    debates: List[DebateHistoryItem]

class PersonaListItem(BaseModel):
    id: int
    topic: str
    name1: str
    name2: str
    persona1_name: str
    persona2_name: str
    persona1_system_prompt: str
    persona2_system_prompt: str
    answer_length: int
    provider: str
    created_at: datetime

class PersonaListResponse(BaseModel):
    personas: List[PersonaListItem]