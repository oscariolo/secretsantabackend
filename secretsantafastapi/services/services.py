from sqlalchemy.orm import Session

from domain import models

def get_room(db: Session, room_id: str):
    return db.query(models.Room).filter(models.Room.id == room_id).first()

def get_secret_santa_for(db: Session, room_id: str, participant_id: int):
    participant = db.query(models.Participant).filter(models.Participant.id == participant_id, models.Participant.room_id == room_id).first()
    if participant and participant.secret_santa_for:
        return participant.secret_santa_for.name
    return None
