from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

class StudentOut(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: EmailStr
    password: str

class StudentIn(BaseModel):
    email: EmailStr
    password: str

class ClassOut(BaseModel):
    subject: str
    date: datetime
