from typing import Any, Union
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel

from app.schemas.general import ResponseSuccess, ResponseError
from ..models import user
from ..schemas.user import UserFull
from sqlalchemy.orm import Session
from ..db import SessionLocal

users = APIRouter(prefix="/user", tags=["user"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class User(BaseModel):
    user: UserFull


class UserResponse(ResponseSuccess):
    data: User


@users.get("/{user_id}", response_model=Union[UserResponse, ResponseError])
def get_user(user_id: int, db: Session = Depends(get_db)):

    if user_db := user.get_user_by_id(db, user_id):
        return UserResponse(data=User(user=user_db))

    return ResponseError(error=f"No user with {user_id=}")


@users.put("/{user_id}", response_model=Union[UserResponse, ResponseError])
def update_user_data(
    picture: bool | None = None,
    email: bool | None = None,
    new_place: bool | None = None,
    score: bool | None = None,
    data: Any = Query(description="The actual data that will replace current"),
):
    return ResponseError(error="Not implemented!")
