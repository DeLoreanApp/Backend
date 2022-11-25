from typing import Any, Union
from fastapi import APIRouter, Depends, Query
from pydantic import EmailStr
from sqlalchemy.orm import Session

from ..schemas import ResponseError, UserResponse
from ..models import user as user_db
from ..db import SessionLocal

users = APIRouter(prefix="/user", tags=["user"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@users.get("/{user_id}", response_model=Union[UserResponse, ResponseError])
def get_user(user_id: int, db: Session = Depends(get_db)):

    if user := user_db.get_user_by_id(db, user_id):
        return UserResponse(user=user)

    return ResponseError(error=f"No user with {user_id=}")

@users.put("/{user_id}/email", response_model=Union[UserResponse, ResponseError])
def update_user_email(user_id: int, new_email: EmailStr):

    if result := user_db.update_email(user_id, new_email):
        return UserResponse(user=result)

    return ResponseError(error=f"User with {user_id} doesn't exist")

@users.post("/{user_id}/places", response_model=Union[UserResponse, ResponseError], tags=["WIP"])
def update_user_places(user_id: int, place_id: int):

    if result := user_db.insert_new_place(user_id, place_id):
        return UserResponse(user=result)

    return ResponseError(error="Not implemented")

@users.put("/{user_id}/picture", response_model=Union[UserResponse, ResponseError], tags=["WIP"])
def update_user_picture(user_id: int, picture: Any):

    if result := user_db.update_picture(user_id, picture):
        return UserResponse(user=result)

    return ResponseError(error="Not implemented")

@users.put("/{user_id}/score", response_model=Union[UserResponse, ResponseError])
def update_user_score(user_id: int, score: int):

    if result := user_db.update_score(user_id, score):
        return UserResponse(user=result)

    return ResponseError(error=f"User with {user_id} doesn't exist")


