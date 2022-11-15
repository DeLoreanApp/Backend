"""
The schemas are used in the API itself. What FastAPI does is converts Python objects from/to JSON (or other formats).
For instance, you receive a login request where we have a username and password as a JSON. You create a schema for this JSON,
 that has fields “username” and “password” and pass it to FastAPI and it does its magic. So to create a schema you need think
 what data will be shared
between api and the app, split them by requests: Base, Login, Registering (might be something else)
"""

from pydantic import BaseModel
from typing import Literal


class UserBase(BaseModel):
    pass


class UserRegister(UserBase):
    email: str
    username: str
    password: str

class UserLogin(UserBase):
    email_or_username: str
    password: str


class User(UserBase):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True

class UserResponseBase(BaseModel):

    status: Literal["success", "fail"]

class UserResponseError(UserResponseBase):

    error: str

class UserResponseSuccess(UserResponseBase):

    data: User
