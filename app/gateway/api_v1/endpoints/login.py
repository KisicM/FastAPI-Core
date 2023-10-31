from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.core.config import Settings, get_settings
import app.gateway.dependencies as deps
from app.repository.user_repository import UserRepository
from app.util import security
from app.model.user import User
from app.model.token import Token

router = APIRouter()


@router.post("/login/access-token", response_model=Token)
def login_access_token(
    user_repository: UserRepository = Depends(deps.get_user_repository),
    form_data: OAuth2PasswordRequestForm = Depends(),
    settings: Settings = Depends(get_settings)
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = user_repository.authenticate(email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user_repository.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, secret_key=settings.SECRET_KEY, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/login/test-token", response_model=User)
def test_token(current_user_id: int = Depends(deps.validate_token)) -> Any:
    """
    Test access token
    """
    return current_user_id
