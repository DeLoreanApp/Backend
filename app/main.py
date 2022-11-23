from typing import Union
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from .models import user as m_user
from .models import monuments
from .db import SessionLocal, engine, Base
from .schemas import user as s_user
from .schemas.general import ResponseSuccess, ResponseError
from .routers.user import users

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(users)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class LoginResponse(BaseModel):
    user: s_user.UserMinimal
    leader_board: list[s_user.UserMinimal]

class UResponse(ResponseSuccess):
    data: LoginResponse

@app.post("/login", response_model=Union[UResponse, ResponseError], response_model_by_alias=True, tags=['user'])
async def login(user: s_user.UserLogin, db: Session = Depends(get_db)):

    if user_db := m_user.auth(db, user):
        leader_board_db = m_user.get_leader_board(db)
        response = LoginResponse(user=user_db, leader_board=leader_board_db)
        return ResponseSuccess(data=response)

    return ResponseError(error="User doesn't exists or password is incorrect")



@app.post("/register", response_model=Union[UResponse, ResponseError], response_model_by_alias=True, tags=["user"])
async def register(user: s_user.UserRegister, db: Session = Depends(get_db)):

    if not m_user.get_user_by_username(db, user.username):

        user_db = m_user.create_user(db, user)
        leader_board_db = m_user.get_leader_board(db)
        response = LoginResponse(user=user_db, leader_board=leader_board_db)
        return ResponseSuccess(data=response)

    return ResponseError(error="User already exists")


