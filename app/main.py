from dotenv import dotenv_values
from fastapi import FastAPI
from .models import SQLModel
from .database_sql import engine
from .middleware import block_unknown_ip_addresses
from .exceptions import not_found
from .routers.student import student_router
from .routers.classes import classes_router
from .routers.home import home_router




SQLModel.metadata.create_all(bind=engine)

app = FastAPI(redoc_url=None)

app.include_router(student_router)
app.include_router(classes_router)
app.include_router(home_router)

app.middleware("http")(block_unknown_ip_addresses)
app.exception_handler(404)(not_found)
