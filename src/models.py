from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, BigInteger, String, DateTime, Text, UniqueConstraint, false
from sqlalchemy.sql.schema import ForeignKey


Base = declarative_base()


class Message(Base):
    __tablename__ = 'message'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nickname = Column(String(32), nullable=False)
    faceimg = Column(String(256), nullable=False)
    gender = Column(String(16), nullable=False)
    social_uid = Column(String(64), nullable=True)
    ip = Column(String(32), nullable=True)
    message = Column(String(512), nullable=False)
    created_time = Column(DateTime, nullable=False)
   
    
class Record(Base):
    __tablename__ = 'record'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    social_uid = Column(String(64), nullable=false)
    message_id = Column(BigInteger, nullable=false)
    
    __table_args__ =(
        UniqueConstraint('social_uid', 'message_id'),
    )