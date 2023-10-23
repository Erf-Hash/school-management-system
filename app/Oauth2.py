from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from datetime import datetime, timedelta
from typing import Annotated
from sqlmodel import Session
from .database_sql import engine
from .models import Student
from hashlib import md5


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
EXPIRE_MINUTES = 720
PASSWORD_SALT = "ABC"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


def create_jwt(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY)


def get_jwt_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    try:
        with Session(engine) as session:
            user = session.get(Student, user_id)
    except:
        raise credentials_exception

    return user


def hash_password(password: str):
    password += PASSWORD_SALT
    hashed = md5(password.encode())
    return hashed.hexdigest()