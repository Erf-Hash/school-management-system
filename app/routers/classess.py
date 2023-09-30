from fastapi import APIRouter


router = APIRouter(
    prefix='/class',
    tags="Class",
)


@router.get("/")
async def read_items():
    return "hello"