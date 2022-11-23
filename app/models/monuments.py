from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import Session

from ..db import Base


class Monument(Base):

    __tablename__ = 'monuments'

    id = Column(Integer, primary_key=True, index=True, autoincrement="auto")
    name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    country = Column(String, nullable=False)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    # game
