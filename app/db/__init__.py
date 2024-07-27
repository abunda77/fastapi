# app/db/__init__.py
from .base import Base
from .database import engine, SessionLocal, get_db

# Create all tables in the database
#Base.metadata.create_all(bind=engine)