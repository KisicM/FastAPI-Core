from ..db.session import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.config import Settings, get_settings
from app.db.schema.user import User
from app.repository.user_repository import UserRepository

def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(User, db)
