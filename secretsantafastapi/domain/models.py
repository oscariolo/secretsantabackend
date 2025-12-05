from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from database.database import Base

class Room(Base):
    __tablename__ = "room"

    id = Column(String, primary_key=True, index=True)
    participants = relationship("Participant", back_populates="room")

class Participant(Base):
    __tablename__ = "participant"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    room_id = Column(String, ForeignKey("room.id"))
    secret_santa_for_id = Column(Integer, ForeignKey("participant.id"))

    room = relationship("Room", back_populates="participants")
    secret_santa_for = relationship("Participant", remote_side=[id])
