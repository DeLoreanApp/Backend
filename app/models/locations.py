from sqlalchemy import Column, Integer, String, Float
from ..db import Base


class Location(Base):
    __tablename__ = "locations"

    location_id = Column(Integer, primary_key=True, index=True, autoincrement="auto")
    location_name = Column(String, unique=True, index=True, nullable=False)
    location_address = Column(String, unique=True, index=True, nullable=False)
    longitude = Column(Float, unique=True, index=True, nullable=False)
    latitude = Column(Float, unique=True, index=True, nullable=False)
    location_description = Column(String, unique=True, index=True, nullable=False)


def get_location_id(db: Session, location_id: int) -> Location | None:
    return db.query(Location).filter(Location.location_id == location_id).first()

def get_location_name(db: Session, location_name: str) -> Location | None:
    return db.query(Location).filter(Location.location_name == location_name).first()

def get_longitude(db: Session, longitude: float) -> Location | None:
    return db.query(Location).filter(Location.longitude == longitude).first()

def get_latitude(db: Session, latitude: float) -> Location | None:
    return db.query(Location).filter(Location.latitude == latitude).first()

def get_location_description(db: Session, location_description: str) -> Location | None:
    return db.query(Location).filter(Location.location_description == location_description).first()

