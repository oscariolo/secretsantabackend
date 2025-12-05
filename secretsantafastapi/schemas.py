from pydantic import BaseModel
from typing import List, Optional

class CreateRoomRequest(BaseModel):
    participants: List[str]

class AddParticipantRequest(BaseModel):
    name: str

class ParticipantResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class RoomResponse(BaseModel):
    id: str
    participants: List[ParticipantResponse]

    class Config:
        from_attributes = True

class RoomListResponse(BaseModel):
    id: str
    participant_count: int

    class Config:
        from_attributes = True
