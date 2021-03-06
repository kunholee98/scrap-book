import datetime
import jwt

from typing import Optional

from fastapi import Depends, Header, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from src.service.user import UserService
from src.sql.models import User
from src.sql.database import get_db

from src.config import Config

def error(code, error = None,ok=False):
    if not error:
        error = Config.ERROR_CODE[code]
    detail = {
        'error': error,
        'ok': ok
    }

    return detail

async def check_token(db: Session = Depends(get_db), refreshToken: Optional[str] = Header(...), accessToken: Optional[str] = Header(...)):
    if not refreshToken or not accessToken:
        return None
    user = UserService.get_user_by_token(db, refreshToken)
    if not user:
        return None
    try:
        token_id = jwt.decode(accessToken, Config.ACCESS_TOKEN_KEY, Config.JWT_ALGORITHM)
        id = token_id['id']
    except jwt.DecodeError as e:
        print(e)
        return None
    if user.id == id:
        return refreshToken
    return None

async def verify_token(
    accesstoken:Optional[str] = Header(None),
    db: Session = Depends(get_db)
    ):
    if not accesstoken:
        return None
    try:
        token_id = jwt.decode(accesstoken, Config.ACCESS_TOKEN_KEY, algorithms=Config.JWT_ALGORITHM)
        id = token_id["id"]
        if not token_id:
            return None
    except jwt.DecodeError as e:
        print(e)
        return None
    except jwt.ExpiredSignatureError as e:
        print(e)
        return None
    current_user = UserService.get_user_by_id(db, id)
    return current_user

