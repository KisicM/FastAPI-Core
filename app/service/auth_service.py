from datetime import timedelta
from typing import Any
from fastapi import Depends
from app.model.token import Token
from app.repository.user_repository import UserRepository
from app.service.dependencies import get_user_repository
from app.util import security
from .dependencies import get_settings, Settings


class AuthService():
    """
    Authorization service
    """
    def __init__(self,
                 user_repository: UserRepository = Depends(get_user_repository),
                 settings: Settings = Depends(get_settings)):
                self.user_repository = user_repository
                self.settings = settings

    def login(self, *, email, password) -> (Token | str):
        user = self.user_repository.authenticate(email=email, password=password)
        if not user:
            return "incorrect_credentials"
        elif not self.user_repository.is_active(user):
            return "user_not_active"
        access_token_expires = timedelta(minutes=self.settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return {
            "access_token": security.create_access_token(
                user.id, secret_key=self.settings.SECRET_KEY, expires_delta=access_token_expires
            ),
            "token_type": "bearer",
        }