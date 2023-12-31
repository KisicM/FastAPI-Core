from typing import TYPE_CHECKING
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from ..base import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)