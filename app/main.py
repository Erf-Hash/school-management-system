from fastapi import FastAPI
from .models import SQLModel
from .database_sql import engine
from .middleware import marg_bar_america
from .exceptions import not_found
from .routers.student import router as student_router
from .routers.classess import router as class_router



SQLModel.metadata.create_all(bind=engine)


app = FastAPI(redoc_url=None)

app.include_router(student_router)
app.include_router(class_router)
app.middleware('http')(marg_bar_america)
app.exception_handler(404)(not_found)
