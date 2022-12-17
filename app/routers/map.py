from typing import Union
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.general import ResponseError
from app.schemas.map import MapORM, ResponseMapORM
from ..db import SessionLocal
from ..models import user_monuments as u_m_db, locations as loc_db

map = APIRouter(prefix="/map", tags=["map"])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@map.get("/{city}", response_model=Union[ResponseMapORM, ResponseError])
def get_all_locations_by_city(city: str, db: Session = Depends(get_db)):

    l = loc_db.get_locations_by_city(db, city)
    m = u_m_db.get_monuments_by_city(db, city)

    return ResponseMapORM(map=MapORM(monuments=m, locations=l))


@map.get("/{country}", response_model=Union[ResponseMapORM, ResponseError])
def get_all_locations_by_country(country: str, db: Session = Depends(get_db)):

    l = loc_db.get_locations_by_country(db, country)
    m = u_m_db.get_monuments_by_country(db, country)

    return ResponseMapORM(map=MapORM(monuments=m, locations=l))
