from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.core.config import Settings, get_settings
import app.gateway.dependencies as deps
from app.repository.user_repository import UserRepository
from app.service.auth_service import AuthService
from app.util import security
from app.model.user import User
from app.model.token import Token

router = APIRouter()


@router.post("/login/access-token", response_model=Token)
def login_access_token(
    auth_service: AuthService = Depends(AuthService),
    form_data: OAuth2PasswordRequestForm = Depends()
    ) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    result = auth_service.login(email=form_data.username, password=form_data.password)
    if result == "incorrect_credentials":
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if result == "user_not_active":
        raise HTTPException(status_code=400, detail="Inactive user")
    return result


@router.post("/login/test-token", response_model=User)
def test_token(current_user_id: int = Depends(deps.validate_token)) -> Any:
    """
    Test access token
    """
    return current_user_id
