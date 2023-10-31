from typing import Any, Dict, Optional, Type, Union
from sqlalchemy.orm import Session
from app.util.security import get_password_hash, verify_password
from .generic_repository import CRUDBase
from app.db.schema.user import User
from app.model.user import UserCreate, UserUpdate


class UserRepository(CRUDBase[User, UserCreate, UserUpdate]):
    def __init__(self, model: type[User], db: Session):
        super().__init__(model, db)

    def get_by_email(self, *, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def create(self, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            is_active=obj_in.is_active
        )
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(self, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data.get("password") is not None:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db_obj=db_obj, obj_in=update_data)

    def authenticate(self, *, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active
