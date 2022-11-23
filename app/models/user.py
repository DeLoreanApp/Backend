from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.sqlite import BLOB
from sqlalchemy.orm import Session
from bcrypt import hashpw, checkpw, gensalt

from ..db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement="auto")
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    score = Column(Integer, default=0)
    picture = Column(BLOB)


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db: Session, username) -> User | None:

    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, user):

    password = hashpw(user.password.encode("utf8"), gensalt())
    db_user = User(email=user.email, hashed_password=password, username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def auth(db: Session, user) -> bool:

    if "@" in user.email_or_username:

        user_db = db.query(User).filter(User.email == user.email_or_username).first()
    else:
        user_db = db.query(User).filter(User.username == user.email_or_username).first()

    if not user_db:
        return None

    if checkpw(user.password.encode("utf8"), user_db.hashed_password):
        return user_db

    return None

def get_leader_board(db: Session) -> list[User]:

    return db.query(User).filter().order_by(User.score.desc()).limit(30).all()
