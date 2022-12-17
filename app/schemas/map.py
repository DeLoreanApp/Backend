from pydantic import BaseModel
from app.schemas.location import LocationORM

from app.schemas.monuments import MonumentORM
from .general import ResponseSuccess


class MapORM(BaseModel):

    monuments: list[MonumentORM] | None
    locations: list[LocationORM] | None


class ResponseMapORM(ResponseSuccess):
    map: MapORM
