from typing import Any, List
from fastapi import Depends
from app.model.user import User, UserCreate, UserUpdate
from app.repository.user_repository import UserRepository
from app.service.dependencies import get_user_repository


class UserService():
    """
    User service
    """
    def __init__(self, user_repository: UserRepository = Depends(get_user_repository)):
        self.user_repository = user_repository


    def read_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        users = self.user_repository.get_multi(skip=skip, limit=limit)
        return users
    

    def create_user(self, *, user_in: UserCreate) -> (User | None):
        user = self.user_repository.get_by_email(email=user_in.email)
        if user:
            return None
        user = self.user_repository.create(obj_in=user_in)
        return user
    

    def read_by_id(self, user_id: int) -> (User | None):
        return self.user_repository.get(id=user_id)
    

    def update_user(self, *, user_id: int, user_in: UserUpdate) -> (User | None):
        user = self.user_repository.get(id=user_id)
        if not user:
            return None
        user = self.user_repository.update(db_obj=user, obj_in=user_in)
        return user
        