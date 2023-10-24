import pytest
from sqlmodel import select, Session
from ..main import app
from ..database_sql import engine


def test_homepage():
    with Session(engine):
        
        Session.add()



