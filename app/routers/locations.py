from typing import Union
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.general import ResponseError
from app.schemas.location import Location, ResponseLocation
from ..db import SessionLocal
from ..models import locations as loc_db

locations = APIRouter(prefix="/location", tags=["locations"])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@locations.put("/", response_model=Union[ResponseLocation, ResponseError])
def add_location(location: Location, db: Session = Depends(get_db)):

    if result := loc_db.add_location(db, location):
        return ResponseLocation(location=result)

    return ResponseError(error="Location already exists")
