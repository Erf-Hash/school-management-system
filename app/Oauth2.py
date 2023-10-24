from dotenv import dotenv_values
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from datetime import datetime, timedelta
from typing import Annotated
from sqlmodel import Session
from hashlib import md5
from .database_sql import engine
from .models.models_student import Student


ENV = dict(dotenv_values(dotenv_path="./environment_variables.env"))
SECRET_KEY = ENV['SECRET_KEY']
EXPIRE_MINUTES = int(ENV['EXPIRE_MINUTES'])
PASSWORD_SALT = ENV["PASSWORD_SALT"]

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
        user_id: str = payload.get('user_id')
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