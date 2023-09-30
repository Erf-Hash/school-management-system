from fastapi import status, HTTPException, Depends, APIRouter
from sqlmodel import Session, select
from fastapi.responses import JSONResponse
from typing import Annotated
from ..database_sql import engine
from ..Oauth2 import get_jwt_user
from ..models import StudentOut, Student


router = APIRouter(
    prefix="/student",
    tags=['Students']
)

# , auth: Annotated[StudentOut, Depends(get_jwt_user)]
@router.get('/{id}', response_model=StudentOut)
def get_student(id: int):
    with Session(engine) as session:
        return session.exec(select(Student).where(Student.id == id)).one()



@router.post('/')
def register_student(user: StudentOut):
    try:
        new_user = Student(**user.dict())
        with Session(engine) as session:
            session.add(new_user)
            session.commit()
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong Credentials")

    return JSONResponse(content="Student was registered successfully", status_code=status.HTTP_201_CREATED)


@router.put('/{id}')
def reform_student(id: int, updated_student: StudentOut):
    try:
        with Session(engine) as session:
            db_user = session.get(Student, id)

            if not db_user:
                raise HTTPException(status_code=404, detail="Student not found")

            updated_user_data = updated_student.dict(exclude_unset=True)
            for key, value in updated_user_data.items():
                setattr(db_user, key, value)

            session.add(db_user)
            session.commit()
            session.refresh(db_user)

            return db_user

    except:
        pass
