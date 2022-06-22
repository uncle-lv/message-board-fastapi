from functools import lru_cache
from pydantic import BaseSettings, AnyHttpUrl


class OAuth2Settings(BaseSettings):
    app_id: str
    app_key: str
    redirect_url: AnyHttpUrl
    
@lru_cache()
def get_qq_oauth() -> OAuth2Settings:
    return OAuth2Settings(app_id='1062', app_key='b37cdc0711eb02e95d6b42fa8ac1f342', redirect_url='http://127.0.0.1:8080')
    