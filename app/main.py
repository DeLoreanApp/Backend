from typing import Union

from fastapi import Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session


from .setup_app import app
from .schemas import UserRegister, UserLogin, UserResponse, ResponseError
from .models import user as user_db
from .db import SessionLocal




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=RedirectResponse, status_code=302, include_in_schema=False)
def redirect_main_to_docs():
    return "/docs"


@app.post(
    "/login",
    response_model=Union[UserResponse, ResponseError],
    response_model_by_alias=True,
    tags=["user"],
)
def login(user: UserLogin, db: Session = Depends(get_db)):

    if user := user_db.auth(db, user):
        return UserResponse(user=user)

    return ResponseError(error="User doesn't exists or password is incorrect")


@app.post(
    "/register",
    response_model=Union[UserResponse, ResponseError],
    response_model_by_alias=True,
    tags=["user"],
)
def register(user: UserRegister, db: Session = Depends(get_db)):

    if not user_db.get_user_by_username(db, user.username):
        user = user_db.create_user(db, user)
        return UserResponse(user=user)

    return ResponseError(error="User already exists")
