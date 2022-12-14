from typing import Union

from fastapi import Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session


from .setup_app import app
from .schemas import UserRegister, UserLogin, UserResponse, ResponseError, LeaderBoard, UserResponseFull
from .models import user_monuments as user_monuments_db
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
    response_model=Union[UserResponseFull, ResponseError],
    response_model_by_alias=True,
    tags=["user"],
)
def login(user: UserLogin, db: Session = Depends(get_db)):
    user, monuments = user_monuments_db.auth(db, user)
    if user:
        return UserResponseFull(user=user, monuments=monuments)

    return ResponseError(error="User doesn't exist or password is incorrect")


@app.post(
    "/register",
    response_model=Union[UserResponse, ResponseError],
    response_model_by_alias=True,
    tags=["user"],
)
def register(user: UserRegister, db: Session = Depends(get_db)):

    if user_monuments_db.get_user_by_username(db, user.username):
        return ResponseError(error="Username already exists")

    if user_monuments_db.get_user_by_email(db, user.email):
        return ResponseError(error="Email already exists")


    user = user_monuments_db.create_user(db, user)
    return UserResponse(user=user)


@app.get("/leaderboard", response_model=Union[LeaderBoard, ResponseError])
async def get_leaderbord(db: Session = Depends(get_db)):

    if result := user_monuments_db.get_leader_board(db):

        return LeaderBoard(leaderboard=result)

    return LeaderBoard(leaderboard=[])

