
from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..schemas.monuments import MonumentCreate
from ..models.monuments import add_new_monument
from ..db import SessionLocal

monuments = APIRouter(prefix="/monument", tags=["monument"])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@monuments.put("/")
def add_new_place(monument: MonumentCreate, db: Session = Depends(get_db)):
    add_new_monument(db, monument)



