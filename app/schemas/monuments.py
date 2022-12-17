from pydantic import BaseModel
from .general import ResponseSuccess


class MonumentCreate(BaseModel):

    name: str
    city: str
    country: str
    lat: float
    lon: float
    description: str


class Monument(BaseModel):

    id: int
    name: str
    city: str
    country: str
    lat: float
    lon: float
    description: str


class MonumentORM(BaseModel):

    id: int
    name: str
    city: str
    country: str
    lat: float
    lon: float
    description: str

    class Config:
        orm_mode = True


class ResponseMonuments(ResponseSuccess):
    monuments: list[MonumentORM]


class ResponseMonument(ResponseSuccess):
    monument: MonumentORM
