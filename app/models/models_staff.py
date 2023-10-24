from sqlmodel import Field
from typing import Optional
from pydantic import EmailStr
from enum import Enum
from .models_student import SQLModel


class Role(Enum):
    PRINCIPAL = 1
    TEACHER = 2
    ASSISTANT = 3


class Status(Enum):
    INACTIVE = 0
    ACTIVE = 1


class Gender(Enum):
    MALE = 1
    FEMALE = 2


class Staff(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    first_name: str
    last_name: str
    password: str
    email: EmailStr
    role: Role
