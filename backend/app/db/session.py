import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

POSTGRES_USER = os.getenv("POSTGRES_USER", "coach")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "coachpw")
POSTGRES_DB = os.getenv("POSTGRES_DB", "code_coach")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "db")
SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
