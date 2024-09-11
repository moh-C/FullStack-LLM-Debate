from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Ensure the /app/data directory exists
os.makedirs("/app/data", exist_ok=True)

# Database for debates
DEBATE_DATABASE_URL = "sqlite:////app/data/debate_history.db"
debate_engine = create_engine(DEBATE_DATABASE_URL, connect_args={"check_same_thread": False})
DebateSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=debate_engine)

# Database for personas
PERSONA_DATABASE_URL = "sqlite:////app/data/personas.db"
persona_engine = create_engine(PERSONA_DATABASE_URL, connect_args={"check_same_thread": False})
PersonaSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=persona_engine)

Base = declarative_base()

def get_debate_db():
    db = DebateSessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_persona_db():
    db = PersonaSessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    from app.models import Base
    Base.metadata.create_all(bind=debate_engine)
    Base.metadata.create_all(bind=persona_engine)