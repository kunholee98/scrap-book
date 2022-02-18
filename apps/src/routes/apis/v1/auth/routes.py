import datetime
from fastapi import APIRouter, Body, Depends, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from src.common.response import verify_token
from src.service.user import UserService
from src.sql.database import get_db
from src.sql.models import User
from .schemas import UserIn, Token

rt = APIRouter(
    prefix='/apis/v1/auth',
    tags=['apis/v1/auth']
)

@rt.post("/signUp", description="회원가입 API", status_code=status.HTTP_201_CREATED)
def sign_up(db: Session = Depends(get_db), user: UserIn = Body(..., embed=True)):
    existed = UserService.get_user_by_email(db, user.email)
    if existed:
        return JSONResponse(content={
            "error": "already existed",
            "ok": False
            }, status_code=status.HTTP_200_OK)

    user_db = UserService.create_user(db, user)
    if user_db:
        json_user_db = jsonable_encoder(user_db)
        print(json_user_db)
        return JSONResponse(content={"user": json_user_db})

@rt.post('/login')
def login(db:Session = Depends(get_db), user: UserIn = Body(..., embed=True)):
    user_db = UserService.get_user_by_email(db, user.email)
    if not user_db:
        return JSONResponse(content={
            "error": "user not existed",
            "ok": False
        })
    user_json = jsonable_encoder(user_db)
    token = UserService.create_refresh_token(db, user_db.id)
    if not token:
        return {"error": "no token", "ok": False}
    headers = UserService.create_access_token(token)
    response = JSONResponse(content={**user_json, "refreshToken":token}, headers=headers)
    response.set_cookie('token', token, httponly=True)
    return response
    

@rt.get('/{id}')
def search(db:Session = Depends(get_db), id: int = 1):
    db_user = db.query(User).filter(User.id == id).first()
    if db_user:
        return db_user
    return {"error": "fail to find an user"}

# @rt.post('/test/{id}', response_model=Token)
@rt.delete('/delete')
def delete(db:Session = Depends(get_db), user: User = Depends(verify_token)):
    return UserService.delete_user(db, user.id)