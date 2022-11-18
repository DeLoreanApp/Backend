"""
The schemas are used in the API itself. What FastAPI does is converts Python objects from/to JSON (or other formats).
For instance, you receive a login request where we have a username and password as a JSON. You create a schema for this JSON,
 that has fields “username” and “password” and pass it to FastAPI and it does its magic. So to create a schema you need think
 what data will be shared
between api and the app, split them by requests: Base, Login, Registering (might be something else)
"""

from pydantic import BaseModel, Field
from typing import Literal


class UserBase(BaseModel):
    username: str
    email: str


class UserRegister(UserBase):
    password: str

class UserLogin(BaseModel):
    email_or_username: str
    password: str


class User(UserBase):

    id: int = Field(..., alias="user_id")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class UserResponseError(BaseModel):

    status: Literal["fail"] = "fail"
    error: str

class UserResponseSuccess(BaseModel):

    status: Literal["success"] = "success"
    data: User
