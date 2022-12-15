from typing import Union
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..schemas.monuments import MonumentCreate
from ..models import user_monuments as u_m_db
from ..schemas import ResponseError, ResponseSuccess, ResponseMonuments, ResponseMonument
from ..db import SessionLocal

monuments = APIRouter(prefix="/monument", tags=["monument"])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@monuments.put("/", response_model=Union[ResponseMonument, ResponseError])
def add_new_place(monument: MonumentCreate, db: Session = Depends(get_db)):
    if result := u_m_db.add_new_monument(db, monument):
        return ResponseMonument(monument=result)
    return ResponseError(error="Monument already exists")

@monuments.get("/{city}", response_model=Union[ResponseMonuments, ResponseError])
def get_monuments_by_city(city: str, db: Session = Depends(get_db)):
    if result := u_m_db.get_monuments_by_city(db, city):
        return ResponseMonuments(monuments=result)

    return ResponseError(error="No such city in the database")


@monuments.get("/{country}", response_model=Union[ResponseMonuments, ResponseError])
def get_monuments_by_country(country: str, db: Session = Depends(get_db)):
    if result := u_m_db.get_monuments_by_country(db, country):
        return ResponseMonuments(monuments=result)

    return ResponseError(error="No such country in the database")

@monuments.get("/{id}", response_model=Union[ResponseMonument, ResponseError])
def get_monument_by_id(id: str, db: Session = Depends(get_db)):
    if result := u_m_db.get_monumet_by_id(db, id):
        return ResponseMonument(monument=result)

    return ResponseError(error=f"No such monument with id={id}")
