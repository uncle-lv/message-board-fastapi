import json
import random
from typing import List
from webbrowser import get
from fastapi import Depends, FastAPI
from sqlalchemy import false
import urllib3
from starlette import status
from loguru import logger
from settings import OAuth2Settings, get_qq_oauth
import database
from sqlalchemy.orm import Session
import models, schemas, crud

app = FastAPI()
http = urllib3.PoolManager()
colors = ['#EF5564', '#9CF0E3', '#F488A8']
logger.add("../log/file_{time}.log")

@app.on_event('startup')
async def startup():
    await database.database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.database.disconnect()


@app.get('/login')
async def login(type: str, settings: OAuth2Settings = Depends(get_qq_oauth)):
    response = http.request('GET', f'https://login.uz6.cn/connect.php?act=login&appid={settings.app_id}&appkey={settings.app_key}&type={type}&redirect_uri={settings.redirect_url}')
    json_data = json.loads(response.data.decode('utf-8'))
    return json_data

@app.get('/getUserInfo')
async def get_user_info(code: str, settings: OAuth2Settings = Depends(get_qq_oauth)):
    response = http.request('GET', f'https://login.uz6.cn/connect.php?act=callback&appid={settings.app_id}&appkey={settings.app_key}&type=qq&code={code}')
    json_data = json.loads(response.data.decode('utf-8'))
    logger.debug(json_data)
    return json_data

@app.get('/total')
async def get_user_info(db: Session = Depends(database.get_db)):
    return { 'total': crud.count_message(db) }

@app.get('/messages', response_model=List[schemas.MessageOut], status_code=status.HTTP_200_OK)
async def get_messages(social_uid: str, db: Session = Depends(database.get_db)):
    messages = crud.get_messages(db)
    for message in messages:
        message.like_count = crud.count_like(message.id, db)
        message.is_liked = crud.is_like(social_uid, message.id, db)
        message.color = get_random_color()
    
    return messages

@app.post('/messages', status_code=status.HTTP_201_CREATED)
async def create_message(message: schemas.MessageCreate, db: Session = Depends(database.get_db)):
    crud.create_message(message, db)
    
@app.post('/like', status_code=status.HTTP_200_OK)
async def like_message(like: schemas.Like, db: Session = Depends(database.get_db)):
    crud.mark_like(like, db)

def get_random_color():
    return random.choice(colors)
