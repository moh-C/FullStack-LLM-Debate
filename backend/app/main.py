from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.routes import debate, websocket
from app.database import create_tables, get_persona_db
from app.models import Persona
from app.schemas import PersonaListResponse, PersonaListItem

# Create database tables
create_tables()

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(debate.router)
app.include_router(websocket.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Debate API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/personas", response_model=PersonaListResponse)
async def list_personas(db: Session = Depends(get_persona_db)):
    personas = db.query(Persona).all()
    return PersonaListResponse(
        personas=[
            PersonaListItem(
                id=persona.id,
                topic=persona.topic,
                name1=persona.name1,
                name2=persona.name2,
                persona1_name=persona.persona1_name,
                persona2_name=persona.persona2_name,
                persona1_system_prompt=persona.persona1_system_prompt,
                persona2_system_prompt=persona.persona2_system_prompt,
                answer_length=persona.answer_length,
                provider=persona.provider,
                created_at=persona.created_at
            )
            for persona in personas
        ]
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)