from datetime import datetime

from fastapi import Request
from sqlalchemy import (
    TIMESTAMP,
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from src.database.db import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    users = relationship("User", back_populates="role")

    def __str__(self) -> str:
        return f"Role {self.name}"

    def __admin_repr__(self, request: Request) -> str:
        return str(self)

    async def __admin_select2_repr__(self, request: Request) -> str:
        return f"<span>{str(self)}</span>"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True)
    hashed_password: str = Column(String(length=1024), nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)

    role_id = Column(Integer, ForeignKey("roles.id"), default=1)
    role = relationship("Role", back_populates="users")

    def __str__(self) -> str:
        return f"User: {self.username}"

    async def __admin_repr__(self, request: Request) -> str:
        return str(self)

    async def __admin_select2_repr__(self, request: Request) -> str:
        return f"<span>User(id={self.id}, email={self.email})</span>"
