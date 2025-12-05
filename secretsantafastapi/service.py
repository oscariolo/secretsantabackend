import uuid
import random
from sqlalchemy.orm import Session
from models import Room, Participant
from typing import List, Optional

class SecretSantaService:
    
    @staticmethod
    def create_room(db: Session, participant_names: List[str]) -> Room:
        room = Room(id=str(uuid.uuid4()))
        db.add(room)
        db.flush()
        
        participants = []
        for name in participant_names:
            participant = Participant(name=name, room_id=room.id)
            participants.append(participant)
            db.add(participant)
        
        db.flush()
        SecretSantaService._assign_secret_santas(participants)
        
        db.commit()
        db.refresh(room)
        return room
    
    @staticmethod
    def _assign_secret_santas(participants: List[Participant]):
        if len(participants) < 2:
            return 

        if any(p.id is None for p in participants):
            raise ValueError("All participants must have IDs before assignment")
        
        shuffled = participants.copy()
        random.shuffle(shuffled)
        
        for i in range(len(shuffled)):
            shuffled[i].secret_santa_for_id = shuffled[(i + 1) % len(shuffled)].id
    
    @staticmethod
    def get_room(db: Session, room_id: str) -> Optional[Room]:
        return db.query(Room).filter(Room.id == room_id).first()
    
    @staticmethod
    def get_all_rooms(db: Session) -> List[Room]:
        return db.query(Room).all()
    
    @staticmethod
    def delete_room(db: Session, room_id: str) -> bool:
        try:
            room = db.query(Room).filter(Room.id == room_id).first()
            if not room:
                return False
            db.query(Participant).filter(Participant.room_id == room_id).delete()
            db.delete(room)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            print(f"Error deleting room: {str(e)}")
            import traceback
            traceback.print_exc()
            raise e
    
    @staticmethod
    def shuffle_room(db: Session, room_id: str) -> Optional[Room]:
        room = SecretSantaService.get_room(db, room_id)
        if not room:
            return None
        participants = db.query(Participant).filter(Participant.room_id == room_id).all()
        
        if len(participants) < 2:
            return room
        for participant in participants:
            participant.secret_santa_for_id = None
        
        db.flush()
        SecretSantaService._assign_secret_santas(participants)
        db.commit()
        db.refresh(room)
        return room
    
    @staticmethod
    def add_participant(db: Session, room_id: str, participant_name: str) -> Optional[Room]:
        room = SecretSantaService.get_room(db, room_id)
        if not room:
            return None
        new_participant = Participant(name=participant_name, room_id=room_id)
        db.add(new_participant)
        db.flush()
        all_participants = db.query(Participant).filter(Participant.room_id == room_id).all()
        for participant in all_participants:
            participant.secret_santa_for_id = None
        
        db.flush()
        SecretSantaService._assign_secret_santas(all_participants)
        
        db.commit()
        db.refresh(room)
        return room
    
    @staticmethod
    def get_secret_santa_for(db: Session, room_id: str, participant_id: int) -> Optional[str]:
        room = SecretSantaService.get_room(db, room_id)
        if not room:
            return None
        
        for participant in room.participants:
            if participant.id == participant_id and participant.secret_santa_for:
                return participant.secret_santa_for.name
        
        return None
