from pydantic import BaseModel
from .general import ResponseSuccess

class Location(BaseModel):

    location_name: str
    location_address: str
    longitude: float
    latitude: float
    location_description: str
    city: str
    country: str

class LocationORM(BaseModel):
    location_id: int
    location_name: str
    location_address: str
    longitude: float
    latitude: float
    location_description: str
    city: str
    country: str

    class Config:
        orm_mode = True

class ResponseLocation(ResponseSuccess):

    location: LocationORM

class ResponseLocations(ResponseSuccess):

    locations: list[LocationORM]
