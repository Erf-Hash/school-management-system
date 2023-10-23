from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse
from typing import Annotated
from sqlmodel import Session, select
from ..database_sql import engine
from ..models import Student
from ..Oauth2 import hash_password, create_jwt

home_router = APIRouter()


@home_router.post("/login")
def login(user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()]):
    with Session(engine) as session:
        user = session.exec(
            select(Student).where(Student.email == user_credentials.username)
        ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials"
        )   

    if not (hash_password(user_credentials.password) == user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials"
        )


    access_token = create_jwt(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}


@home_router.get(path="/")
async def homepage():
    html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>School Management System</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f0f0f0;
                    margin: 0;
                    padding: 0;
                }
                header {
                    background-color: #3498db;
                    color: #fff;
                    padding: 20px;
                    text-align: center;
                }
                h1 {
                    margin: 0;
                }
                nav {
                    background-color: #333;
                    color: #fff;
                    text-align: center;
                    padding: 10px;
                }
                nav a {
                    color: #fff;
                    text-decoration: none;
                    margin: 10px;
                }
                .container {
                    max-width: 1200px;
                    margin: 20px auto;
                    background-color: #fff;
                    padding: 20px;
                    border-radius: 5px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
                }
                .main-content {
                    padding: 20px;
                }
                .info-card {
                    background-color: #fff;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    padding: 15px;
                    margin: 10px;
                    text-align: center;
                    box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
                }
                footer {
                    background-color: #333;
                    color: #fff;
                    text-align: center;
                    padding: 10px;
                }
            </style>
        </head>
        <body>
            <header>
                <h1>Welcome to Our School Management System</h1>
            </header>
            <nav>
                <a href="#">Home</a>
                <a href="#">Courses</a>
                <a href="#">Students</a>
                <a href="#">Teachers</a>
                <a href="#">Contact</a>
            </nav>
            <div class="container">
                <div class="main-content">
                    <div class="info-card">
                        <h2>About Us</h2>
                        <p>Welcome to our school management system. We are committed to providing quality education and efficient school management services.</p>
                    </div>
                    <div class="info-card">
                        <h2>Latest News</h2>
                        <p>Stay updated with the latest news and events happening in our school.</p>
                    </div>
                    <div class="info-card">
                        <h2>Contact Us</h2>
                        <p>If you have any questions or need assistance, feel free to contact us.</p>
                    </div>
                </div>
            </div>
            <footer>
                &copy; 2023 School Management System
            </footer>
        </body>
        </html>
    """

    return HTMLResponse(content=html, status_code=status.HTTP_201_CREATED)
