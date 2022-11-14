from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from bcrypt import hashpw, checkpw, gensalt

from db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement="auto")
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email_or_username(db: Session, email: str = None, username: str = None) -> User | None:

    if username and email:
        raise ValueError("Either email or username can be specified. Not both")

    if username:
        return db.query(User).filter(User.username == username).first()

    if email:
        return db.query(User).filter(User.email == email).first()

    raise ValueError("Email or username must be specified")

def create_user(db: Session, user) -> None:

    password = hashpw(user.password.encode("utf8"), gensalt())
    db_user = User(email=user.email, hashed_password=password, username=user.username)
    db.add(db_user)
    db.commit()
    # db.refresh(db_user)
    return

def auth(db: Session, user) -> bool:

    if user.email and user.username or not user.email and not user.username:
        raise ValueError()

    if user.email:
        user_db = db.query(User).filter(User.email == user.email).first()
    else:
        user_db = db.query(User).filter(User.username == user.username).first()

    if not user_db:
        return False

    if checkpw(user.password.encode("utf8"), user_db.hashed_password):
        return True

    return False

