from fastapi import FastAPI, Depends, HTTPException, Response
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from database import get_db, init_db
from schemas import (
    CreateRoomRequest, 
    AddParticipantRequest,
    RoomResponse, 
    RoomListResponse
)
from service import SecretSantaService

app = FastAPI(title="Secret Santa API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/api/secret-santa/healthcheck")
async def health_check():
    return "OK"

@app.get("/api/secret-santa/rooms", response_model=List[RoomListResponse])
async def get_all_rooms(db: Session = Depends(get_db)):
    """Get a list of all Secret Santa rooms"""
    rooms = SecretSantaService.get_all_rooms(db)
    return [
        RoomListResponse(
            id=room.id, 
            participant_count=len(room.participants)
        ) 
        for room in rooms
    ]

@app.delete("/api/secret-santa/room/{room_id}", status_code=204)
async def delete_room(room_id: str, db: Session = Depends(get_db)):
    """Delete a Secret Santa room"""
    try:
        success = SecretSantaService.delete_room(db, room_id)
        if not success:
            raise HTTPException(status_code=404, detail="Room not found")
        return Response(status_code=204)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete room: {str(e)}")

@app.post("/api/secret-santa/room/{room_id}/shuffle", response_model=RoomResponse)
async def shuffle_room(room_id: str, db: Session = Depends(get_db)):
    """Re-shuffle Secret Santa assignments for a room"""
    try:
        room = SecretSantaService.shuffle_room(db, room_id)
        if not room:
            raise HTTPException(status_code=404, detail="Room not found")
        return room
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to shuffle: {str(e)}")

@app.post("/api/secret-santa/room/{room_id}/participant", response_model=RoomResponse)
async def add_participant(
    room_id: str, 
    request: AddParticipantRequest,
    db: Session = Depends(get_db)
):
    """Add a new participant to an existing room (re-shuffles assignments)"""
    room = SecretSantaService.add_participant(db, room_id, request.name)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

@app.post("/api/secret-santa/room", status_code=201)
async def create_room(request: CreateRoomRequest, db: Session = Depends(get_db)):
    """Create a new Secret Santa room"""
    room = SecretSantaService.create_room(db, request.participants)
    room_url = f"/api/secret-santa/room/{room.id}"
    return JSONResponse(
        content=room_url,
        status_code=201,
        headers={"Location": room_url}
    )

@app.get("/api/secret-santa/room/{room_id}", response_model=RoomResponse)
async def get_room(room_id: str, db: Session = Depends(get_db)):
    """Get room details"""
    room = SecretSantaService.get_room(db, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

@app.get("/api/secret-santa/room/{room_id}/participant/{participant_id}")
async def get_secret_santa(
    room_id: str, 
    participant_id: int, 
    db: Session = Depends(get_db)
):
    """Get who a participant is Secret Santa for"""
    secret_santa = SecretSantaService.get_secret_santa_for(db, room_id, participant_id)
    if not secret_santa:
        raise HTTPException(status_code=404, detail="Participant not found")
    return secret_santa

