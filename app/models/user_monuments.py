from __future__ import annotations
from typing import Any
from sqlalchemy import Column, Integer, String, LargeBinary, Float, ForeignKey, Table
from sqlalchemy.orm import Session, relationship, Mapped
from bcrypt import hashpw, checkpw, gensalt
from ..schemas import UserLogin, UserRegister
from ..schemas.monuments import MonumentCreate

from ..db import Base


#  ██    ██ ██ ███████ ██ ████████ ███████ ██████      ██████  ██       █████   ██████ ███████ ███████
#  ██    ██ ██ ██      ██    ██    ██      ██   ██     ██   ██ ██      ██   ██ ██      ██      ██
#  ██    ██ ██ ███████ ██    ██    █████   ██   ██     ██████  ██      ███████ ██      █████   ███████
#   ██  ██  ██      ██ ██    ██    ██      ██   ██     ██      ██      ██   ██ ██      ██           ██
#    ████   ██ ███████ ██    ██    ███████ ██████      ██      ███████ ██   ██  ██████ ███████ ███████
#
#

visited_places = Table(
    "visited_places",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("monument_id", ForeignKey("monuments.id"), primary_key=True),
)


#  ███    ███  ██████  ███    ██ ██    ██ ███    ███ ███████ ███    ██ ████████
#  ████  ████ ██    ██ ████   ██ ██    ██ ████  ████ ██      ████   ██    ██
#  ██ ████ ██ ██    ██ ██ ██  ██ ██    ██ ██ ████ ██ █████   ██ ██  ██    ██
#  ██  ██  ██ ██    ██ ██  ██ ██ ██    ██ ██  ██  ██ ██      ██  ██ ██    ██
#  ██      ██  ██████  ██   ████  ██████  ██      ██ ███████ ██   ████    ██
#
#


class Monument(Base):

    __tablename__ = "monuments"

    id = Column(Integer, primary_key=True, index=True, autoincrement="auto")
    name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    country = Column(String, nullable=False)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    visitors: Mapped[list[User]] = relationship(
        "User", secondary=visited_places, back_populates="visited"
    )


def add_new_monument(db: Session, monument: MonumentCreate):

    if get_monument_by_name(db, name=monument.name, city=monument.city):
        return None

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
    db.refresh(m)
    return m


def get_monument_by_name(db: Session, name: str, city: str):
    return (
        db.query(Monument)
        .filter(Monument.name == name)
        .filter(Monument.city == city)
        .first()
    )


def get_monuments_by_city(db: Session, city: str) -> list[Monument]:

    return db.query(Monument).filter(Monument.city == city).all()


def get_monument_by_id(db: Session, id: int) -> Monument:

    return db.query(Monument).filter(Monument.id == id).first()


def get_monuments_by_country(db: Session, country: str) -> list[Monument]:

    return db.query(Monument).filter(Monument.country == country).all()


#  ██    ██ ███████ ███████ ██████
#  ██    ██ ██      ██      ██   ██
#  ██    ██ ███████ █████   ██████
#  ██    ██      ██ ██      ██   ██
#   ██████  ███████ ███████ ██   ██
#


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement="auto")
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    score = Column(Integer, default=0)
    picture = Column(LargeBinary)
    visited: Mapped[list[Monument]] = relationship(
        "Monument", secondary=visited_places, back_populates="visitors"
    )


def get_user_monuments(db: Session, user_id: int) -> list[Monument] | None:

    return (
        db.query(Monument)
        .join(visited_places)
        .filter(visited_places.c.user_id == user_id)
        .all()
    )


def get_user_by_id(db: Session, user_id: int) -> tuple[User, list[Monument]] | None:

    user = db.query(User).filter(User.id == user_id).first()
    monuments = get_user_monuments(db, user_id)

    return user, monuments


def check_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username) -> User | None:

    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, user: UserRegister):

    password = hashpw(user.password.encode("utf8"), gensalt())
    db_user = User(
        email=user.email,
        hashed_password=password.decode("utf8"),
        username=user.username,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def auth(db: Session, user: UserLogin) -> User | None:

    if "@" in user.email_or_username:

        user_db = db.query(User).filter(User.email == user.email_or_username).first()
    else:
        user_db = db.query(User).filter(User.username == user.email_or_username).first()

    if not user_db:
        return None

    if checkpw(user.password.encode("utf8"), user_db.hashed_password.encode("utf8")):
        return user_db

    return None


def get_leader_board(db: Session) -> list[tuple[int, str]]:

    return (
        db.query(User.username, User.score)
        .filter()
        .order_by(User.score.desc())
        .limit(30)
        .all()
    )


def update_email(db: Session, user_id: int, email: str) -> User | None:

    if user := db.query(User).filter(User.id == user_id).first():
        user.email = email
        db.commit()
        db.refresh(user)
        return user
    return None


def update_password(db: Session, user_id: int, password: str) -> User | None:

    hash_password = hashpw(password.encode("utf8"), gensalt())
    if user := db.query(User).filter(User.id == user_id).first():
        user.hashed_password = hash_password.decode("utf8")
        db.commit()
        return user
    return None


def update_score(db: Session, user_id: int, score: int) -> User | None:

    if user := db.query(User).filter(User.id == user_id).first():
        user.score = score
        db.commit()
        db.refresh(user)
        return user
    return None


# TODO: implement
def update_picture(db: Session, user_id: int, picture: Any) -> User | None:
    return None


def insert_new_place(
    db: Session, user_id: int, place_id: int
) -> tuple[User, list[Monument]] | None:

    m = db.query(Monument).filter(Monument.id == place_id).first()

    u = db.query(User).filter(User.id == user_id).first()
    u.visited.append(m)
    db.add(u)
    db.commit()

    return get_user_by_id(db, user_id)
