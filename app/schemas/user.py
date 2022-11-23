"""
The schemas are used in the API itself. What FastAPI does is converts Python objects from/to JSON (or other formats).
For instance, you receive a login request where we have a username and password as a JSON. You create a schema for this JSON,
 that has fields “username” and “password” and pass it to FastAPI and it does its magic. So to create a schema you need think
 what data will be shared
between api and the app, split them by requests: Base, Login, Registering (might be something else)
"""

from pydantic import BaseModel, Field, EmailStr
from .monuments import Monument



class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email_or_username: str
    password: str

class UserMinimal(BaseModel):

    id: int = Field(..., alias="user_id")
    score: int
    profile_picture: bytes | None = Field(unicode_safe=False)

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

class UserFull(UserMinimal):

    vitited_places: list[Monument] | None


