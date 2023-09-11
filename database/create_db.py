"""for testing purposes, this is to be run for installation only"""
from sqlalchemy import create_engine
from models import Base

DATABASE_PATH = "sqlite:///database/test.db"

engine = create_engine(DATABASE_PATH, echo=True)
Base.metadata.create_all(engine)