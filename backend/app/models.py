from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Debate(Base):
    __tablename__ = "debates"

    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String, index=True)
    name1 = Column(String)
    name2 = Column(String)
    provider = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    questions = Column(Text)  # Store as JSON string
    answer_length = Column(Integer)
    persona1 = Column(Text)  # Store as JSON string
    persona2 = Column(Text)  # Store as JSON string
    turns = relationship("DebateTurn", back_populates="debate")

class DebateTurn(Base):
    __tablename__ = "debate_turns"

    id = Column(Integer, primary_key=True, index=True)
    debate_id = Column(Integer, ForeignKey("debates.id"))
    speaker = Column(String)
    content = Column(Text)
    prompt = Column(Text)  # New field to store the prompt
    turn_number = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    debate = relationship("Debate", back_populates="turns")