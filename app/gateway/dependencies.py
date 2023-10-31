import logging
from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
from app.core.config import Settings, get_settings
from app.db.schema.user import User
from app.model.token import TokenPayload
from app.repository.user_repository import UserRepository
from app.util import security
from app.db.session import SessionLocal

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"api/v1/login/access-token"
)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(User, db)


def validate_token(token: str = Depends(reusable_oauth2), settings: Settings = Depends(get_settings)) -> int:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=security.ALGORITHM
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError) as ex:
        print(ex)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials.",
        )
    return token_data.sub
