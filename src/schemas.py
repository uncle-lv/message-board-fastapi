from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class MessageBase(BaseModel):
    nickname: str
    faceimg: str
    message: str
    
class MessageCreate(MessageBase):
    gender: str
    social_uid: str
    ip: str
    
class MessageOut(MessageBase):
    id: int
    like_count: int
    is_liked: Optional[bool] = False
    color: str
    
    class Config:
        orm_mode = True
        
class Like(BaseModel):
    social_uid: str
    message_id: int