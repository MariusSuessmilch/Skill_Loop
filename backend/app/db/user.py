from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from .session import Base
from fastapi_users import schemas

class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    coding_level: Mapped[int] = mapped_column(Integer, default=0)

# FastAPI Users schemas
class UserRead(schemas.BaseUser[int]):
    coding_level: int

class UserCreate(schemas.BaseUserCreate):
    coding_level: int = 0
