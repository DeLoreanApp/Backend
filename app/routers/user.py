from typing import Union
from fastapi import APIRouter, Depends, Query, File, UploadFile
from pydantic import EmailStr
from sqlalchemy.orm import Session

from ..schemas import (
    ResponseError,
    UserResponse,
    NotImplementedResponse,
    UserResponseFull,
)
from ..models import user_monuments as user_monuments_db
from ..db import SessionLocal

users = APIRouter(prefix="/user", tags=["user"])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@users.get("/{user_id}", response_model=Union[UserResponseFull, ResponseError])
async def get_user(user_id: int, db: Session = Depends(get_db)):

    user, monuments = user_monuments_db.get_user_by_id(db, user_id)

    if user and monuments:
        return UserResponseFull(user=user, visited=monuments)

    return ResponseError(error=f"No user with {user_id=}")


@users.put("/{user_id}/email", response_model=Union[UserResponse, ResponseError])

async def update_user_email(
    user_id: int, new_email: EmailStr, db: Session = Depends(get_db)
):

    if result := user_monuments_db.update_email(db, user_id, new_email):
        return UserResponse(user=result)

    return ResponseError(error=f"User with {user_id} doesn't exist")



@users.post(
    "/{user_id}/places",
    response_model=Union[UserResponseFull, ResponseError],
)
async def update_user_places(
    user_id: int, place_id: int, db: Session = Depends(get_db)
):


    user, monuments = user_monuments_db.insert_new_place(db, user_id, place_id)


    if user and monuments:
        return UserResponseFull(user=user, visited=monuments)

    return ResponseError(error=f"No user with {user_id=}")



@users.put(
    "/{user_id}/picture",
    response_model=Union[NotImplementedResponse, UserResponse, ResponseError],
    tags=["WIP"],
)
async def update_user_picture(user_id: int, picture: UploadFile):

    content = await picture.read()

    with open(f"../../files/profile_pictures/{user_id}.jpg", "wb") as file:

        file.write(content)


@users.put("/{user_id}/score", response_model=Union[UserResponse, ResponseError])
async def update_user_score(user_id: int, score: int, db: Session = Depends(get_db)):


    if result := user_monuments_db.update_score(db, user_id, score):
        return UserResponse(user=result)

    return ResponseError(error=f"User with {user_id} doesn't exist")

@users.put("/{user_id}/password", response_model=Union[UserResponse, ResponseError])
async def update_user_password(user_id: int, password: str, db: Session = Depends(get_db)):

    if result := user_monuments_db.update_password(db, user_id, password):
        return UserResponse(user=result)

    return ResponseError(error=f"User with {user_id} doesn't exist")


# @users.get("/leaderboard", response_model=Union[LeaderBoard, ResponseError])
# async def get_leaderbord(db: Session = Depends(get_db)):
#
#     if result := user_db.get_leader_board(db):
#
#         return LeaderBoard(leaderboard=result)

