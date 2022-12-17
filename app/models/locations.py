from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import Session
from ..schemas import location as s_loc
from ..db import Base


class Location(Base):
    __tablename__ = "locations"

    location_id = Column(Integer, primary_key=True, index=True, autoincrement="auto")
    location_name = Column(String, index=True, nullable=False)
    location_address = Column(String, unique=True, index=True, nullable=False)
    longitude = Column(Float, unique=True, index=True, nullable=False)
    latitude = Column(Float, unique=True, index=True, nullable=False)
    location_description = Column(String, unique=True, index=True, nullable=False)
    city = Column(String, index=True, nullable=False)
    country = Column(String, index=True, nullable=False)


def add_location(db: Session, location: s_loc.Location):

    if get_location_name(db, location_name=location.location_name, city=location.city):
        return None

    l = Location(
        location_name=location.location_name,
        location_address=location.location_address,
        longitude=location.longitude,
        latitude=location.latitude,
        location_description=location.location_description,
        city=location.city,
        country=location.country,
    )

    db.add(l)
    db.commit()
    db.refresh(l)
    return l


def get_location_id(db: Session, location_id: int) -> Location | None:
    return db.query(Location).filter(Location.location_id == location_id).first()


def get_location_name(db: Session, location_name: str, city: str) -> Location | None:
    return (
        db.query(Location)
        .filter(Location.location_name == location_name)
        .filter(Location.city == city)
        .first()
    )


def get_longitude(db: Session, longitude: float) -> Location | None:
    return db.query(Location).filter(Location.longitude == longitude).first()


def get_latitude(db: Session, latitude: float) -> Location | None:
    return db.query(Location).filter(Location.latitude == latitude).first()


def get_location_description(db: Session, location_description: str) -> Location | None:
    return (
        db.query(Location)
        .filter(Location.location_description == location_description)
        .first()
    )


def get_locations_by_city(db: Session, city: str) -> list[Location] | None:
    return db.query(Location).filter(Location.city == city).all()


def get_locations_by_country(db: Session, country: str) -> list[Location] | None:
    return db.query(Location).filter(Location.country == country).all()
