from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from app.model.user import User, UserCreate, UserUpdate
import app.gateway.dependencies as deps
from app.repository.user_repository import UserRepository

router = APIRouter()


@router.get("/", response_model=List[User])
def read_users(
    user_repository: UserRepository = Depends(deps.get_user_repository),
    skip: int = 0,
    limit: int = 100,
    current_user_id: int = Depends(deps.validate_token)) -> Any:
    """
    Retrieve users.
    """
    users = user_repository.get_multi(skip=skip, limit=limit)
    return users


@router.post("/", response_model=User)
def create_user(
    *,
    user_repository: UserRepository = Depends(deps.get_user_repository),
    user_in: UserCreate,
    # current_user_id: int = Depends(deps.validate_token)
    ) -> Any:
    """
    Create new user.
    """
    user = user_repository.get_by_email(email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = user_repository.create(obj_in=user_in)
    return user


@router.get("/{user_id}", response_model=User)
def read_user_by_id(
    user_id: int,
    user_repository: UserRepository = Depends(deps.get_user_repository),
    current_user_id: int = Depends(deps.validate_token),
) -> Any:
    """
    Get a specific user by id.
    """
    if user_id != current_user_id:
        raise HTTPException(
            status_code=401,
            detail="Cannot get other user's profile"
        )
    user = user_repository.get(id=user_id)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="User does not exist in the system",
        )
    # TODO: CHECK PRIVILEGE
    return user


@router.put("/{user_id}", response_model=User)
def update_user(
    *,
    user_repository: UserRepository = Depends(deps.get_user_repository),
    user_id: int,
    user_in: UserUpdate,
    current_user_id: int = Depends(deps.validate_token),
) -> Any:
    """
    Update a user.
    """
    if user_id != current_user_id:
        raise HTTPException(
            status_code=401,
            detail="Cannot update other user's profile"
        )
    user = user_repository.get(id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User does not exist in the system",
        )
    user = user_repository.update(db_obj=user, obj_in=user_in)
    return user
