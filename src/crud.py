from datetime import datetime
from sqlalchemy.orm import Session

import models, schemas


def get_messages(db: Session):
    return db.query(models.Message).all()

def create_message(message: schemas.MessageCreate, db: Session) -> None:
    db_message = models.Message(
        nickname=message.nickname,
        faceimg=message.faceimg,
        gender=message.gender,
        social_uid=message.social_uid,
        ip=message.ip,
        message=message.message,
        created_time=datetime.utcnow()
    )
    
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    
def count_message(db: Session) -> int:
    return db.query(models.Message).count()
    
def count_like(id: int, db: Session) -> int:
    return db.query(models.Record).filter(models.Record.message_id==id).count()

def is_like(social_uid: str, message_id: int, db: Session) -> int:
    return db.query(models.Record).filter(models.Record.social_uid==social_uid, models.Record.message_id==message_id).count()

def mark_like(like: schemas.Like, db: Session) -> None:
    db_record = models.Record(
        social_uid=like.social_uid,
        message_id=like.message_id
    )
    
    db.add(db_record)
    db.commit()
    db.refresh(db_record)