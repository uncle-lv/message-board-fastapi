from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import databases

import models


DATABASE_URL = "mysql+pymysql://uncle-lv:uncle-lv123456@101.32.179.230:3306/message_board?charset=utf8mb4"
database = databases.Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()