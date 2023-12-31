from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import get_settings

settings = get_settings()
engine = create_engine(settings.DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()