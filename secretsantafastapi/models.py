from sqlalchemy import Column, String, Integer, ForeignKey, BigInteger
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Room(Base):
    __tablename__ = "room"
    
    id = Column(String, primary_key=True)
    participants = relationship("Participant", back_populates="room", cascade="all, delete-orphan")

class Participant(Base):
    __tablename__ = "participant"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    room_id = Column(String, ForeignKey("room.id"), nullable=False)
    secret_santa_for_id = Column(BigInteger, ForeignKey("participant.id"), nullable=True)
    
    room = relationship("Room", back_populates="participants")
    secret_santa_for = relationship("Participant", remote_side=[id], foreign_keys=[secret_santa_for_id])
