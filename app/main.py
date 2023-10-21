from fastapi import FastAPI
from .models import SQLModel
from .database_sql import engine
from .middleware import block_unknown_ip_addresses
from .exceptions import not_found
from .routers.student import router as student_router
from .routers.classess import router as class_router



SQLModel.metadata.create_all(bind=engine)


app = FastAPI(redoc_url=None)

app.include_router(student_router)
app.include_router(class_router)
app.middleware('http')(block_unknown_ip_addresses)
app.exception_handler(404)(not_found)
