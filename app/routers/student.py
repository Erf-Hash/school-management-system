from fastapi import status, HTTPException, Depends, APIRouter
from sqlmodel import Session, select
from fastapi.responses import JSONResponse
from typing import Annotated
from ..database_sql import engine
from ..Oauth2 import get_jwt_user, hash_password
from ..models.models_student import Student
from ..serializers.serializers_student import StudentOut



student_router = APIRouter(
    prefix="/student",
    tags=['Students']
)

# , auth: Annotated[StudentOut, Depends(get_jwt_user)]
@student_router.get('/{id}', response_model=StudentOut, )
def get_student(id: int, auth: Annotated[StudentOut, Depends(get_jwt_user)]):
    with Session(engine) as session:
        return session.exec(select(Student).where(Student.id == id)).one()



@student_router.post('/')
def register_student(user: StudentOut):
    try:
        new_user = Student(**user.dict())
        new_user.password = hash_password(new_user.password)
        
        with Session(engine) as session:

            should_be_none = session.exec(select(Student).where(Student.email == new_user.email)).first()
            if should_be_none is not None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong Credentials")
                
            session.add(new_user)
            session.commit()
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong Credentials")

    return JSONResponse(content="Student was registered successfully", status_code=status.HTTP_201_CREATED)


@student_router.put('/{id}')
def reform_student(id: int, updated_student: StudentOut, auth: Annotated[StudentOut, Depends(get_jwt_user)]):
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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
