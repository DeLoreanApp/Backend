from typing import Union
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .models import user as m_user
from .db import SessionLocal, engine, Base
from .schemas import user as s_user

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/login", response_model=Union[s_user.UserResponseSuccess, s_user.UserResponseError], response_model_by_alias=True)
async def login(user: s_user.UserLogin, db: Session = Depends(get_db)):

    if user_db := m_user.auth(db, user):
        return s_user.UserResponseSuccess(data=user_db)

    return s_user.UserResponseError(error="User doesn't exists or password is incorrect")



@app.post("/register", response_model=Union[s_user.UserResponseSuccess, s_user.UserResponseError], response_model_by_alias=True)
async def register(user: s_user.UserRegister, db: Session = Depends(get_db)):

    if not m_user.get_user_by_username(db, user.username):

        user_db = m_user.create_user(db, user)
        return s_user.UserResponseSuccess(data=user_db)

    return s_user.UserResponseError(error="User already exists")


