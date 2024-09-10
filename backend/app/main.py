from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import debate_router, websocket_router
from app.database import engine, Base

import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(debate_router)
app.include_router(websocket_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Debate API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)