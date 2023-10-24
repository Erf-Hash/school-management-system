from datetime import datetime
from pydantic import BaseModel


class ClassOut(BaseModel):
    subject: str
    date: datetime
