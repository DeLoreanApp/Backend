from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from os import environ

if db_url := environ.get("DATABASE_URL", None):
    DATABASE_URL = db_url
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg2://")
    args = {}
else:
    DATABASE_URL =  "sqlite:///./database.db"
    args = {"check_same_thread": False}
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    DATABASE_URL, connect_args=args
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
