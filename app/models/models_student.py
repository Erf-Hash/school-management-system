from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from pydantic import EmailStr
from datetime import datetime
from enum import Enum


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


class StudentClassLink(SQLModel, table=True):
    class_id: Optional[int] = Field(
        primary_key=True, default=None, foreign_key="class.id"
    )
    student_id: Optional[int] = Field(
        primary_key=True, default=None, foreign_key="student.id"
    )


class Class(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    subject: str
    date: datetime
    students: List["Student"] = Relationship(
        back_populates="classes", link_model=StudentClassLink
    )


class Student(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    first_name: str
    last_name: str
    password: str
    email: EmailStr
    classes: List[Class] = Relationship(
        back_populates="students", link_model=StudentClassLink
    )

    
class Staff(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    first_name: str
    last_name: str
    password: str
    email: EmailStr
    role: Role

