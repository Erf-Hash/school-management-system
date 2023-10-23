from fastapi import APIRouter


classes_router = APIRouter(
    prefix='/classes',
)


@classes_router.get(path='/')
async def read_items():
    return "hello-class"