from sqlalchemy.orm import Session
from ..schemas.monuments import MonumentCreate
from .user import Monument


def add_new_monument(db: Session, monument: MonumentCreate):

    m = Monument(
        name=monument.name,
        city=monument.city,
        country=monument.country,
        lat=monument.lat,
        lon=monument.lon,
        description=monument.description,
    )

    db.add(m)
    db.commit()

