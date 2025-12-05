from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from domain import models

from services import services

from database import schemas
from database.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/secret-santa/health")
async def healthCheck():
    return {"status": "ok"}

@app.get("/api/secret-santa/room/{room_id}", response_model=schemas.Room)
def get_room(room_id: str, db: Session = Depends(get_db)):
    db_room = services.get_room(db, room_id=room_id)
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return db_room

@app.get("/api/secret-santa/room/{room_id}/participant/{participant_id}")
def get_secret_santa(room_id: str, participant_id: int, db: Session = Depends(get_db)):
    secret_santa = services.get_secret_santa_for(db, room_id=room_id, participant_id=participant_id)
    if secret_santa is None:
        raise HTTPException(status_code=404, detail="Participant not found or secret santa not assigned")
    return secret_santa

