import json
from fastapi import Depends, FastAPI
import urllib3
from loguru import logger
from settings import OAuth2Settings, get_qq_oauth

app = FastAPI()
http = urllib3.PoolManager()
logger.add("file_{time}.log")


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