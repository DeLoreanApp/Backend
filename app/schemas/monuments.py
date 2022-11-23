from pydantic import BaseModel

class Monument(BaseModel):

    id: int
    name: str
    city: str
    country: str
    lat: float
    lon: float
    description: str


