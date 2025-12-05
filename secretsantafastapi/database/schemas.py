from pydantic import BaseModel
from typing import List, Optional

class ParticipantBase(BaseModel):
    name: str

class Participant(ParticipantBase):
    id: int

    class Config:
        orm_mode = True

class Room(BaseModel):
    id: str
    participants: List[Participant] = []

    class Config:
        orm_mode = True
