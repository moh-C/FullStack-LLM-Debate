from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import pytz

from .database import Base

def pst_now():
    return datetime.now(pytz.timezone('US/Pacific'))

class Debate(Base):
    __tablename__ = "debates"

    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String, index=True)
    name1 = Column(String)
    name2 = Column(String)
    provider = Column(String)
    created_at = Column(DateTime(timezone=True), default=pst_now)
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
    prompt = Column(Text)
    turn_number = Column(Integer)
    created_at = Column(DateTime(timezone=True), default=pst_now)

    debate = relationship("Debate", back_populates="turns")

class Persona(Base):
    __tablename__ = "personas"

    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String, index=True)
    name1 = Column(String)
    name2 = Column(String)
    persona1_name = Column(String)
    persona2_name = Column(String)
    persona1_system_prompt = Column(Text)
    persona2_system_prompt = Column(Text)
    answer_length = Column(Integer)
    provider = Column(String)
    created_at = Column(DateTime(timezone=True), default=pst_now)