from pydantic import BaseModel

class Locations(BaseModel):
    location_id: int
    location_name: str
    location_address: str
    longitude: float
    latitude: float
    location_description: str
    class Config:
        orn_mode = True


