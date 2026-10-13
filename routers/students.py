

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

#from pydantic import BaseModel, Field

from schemas import StudentCreate

from db import get_db

from models import Student
#from schemas import StudentCreate, StudentResponse

from schemas import StudentCreate, StudentUpdate, StudentResponse


router = APIRouter(

     prefix="/students",

     tags=["Students"]

                )





# Request body validation

#class StudentCreate(BaseModel):

#     name: str = Field(min_length=1, max_length=100)

#     age: int = Field(gt=0)





# CREATE: Add a new student

@router.post("/")

def create_student(

     student: StudentCreate,

     db: Session = Depends(get_db)

              ):

     new_student = Student(

         name=student.name,

         age=student.age

         )


     db.add(new_student)

     db.commit()

     db.refresh(new_student)



     return {

    "id": new_student.id,

    "name": new_student.name,

    "age": new_student.age
          }


# READ: Get all students

@router.get("/", response_model=list[StudentResponse])

def get_students(db: Session = Depends(get_db)):

    return db.query(Student).order_by(Student.id).all()


# READ: Get one student by ID
@router.get("/{student_id}") 
def get_student( 
        student_id: int, 
        db: Session = Depends(get_db) 
        ):
        student = db.query(Student).filter( 
                Student.id == student_id ).first() 
        if student is None: 
            raise HTTPException( 
                    status_code=404, 
                    detail="Student not found" 
                    )

        return student
# UPDATE: Update a student 
@router.put("/{student_id}") 
def update_student( 
        student_id: int, 
        student_data: StudentCreate, 
        db: Session = Depends(get_db) 
  ): 
    student = db.query(Student).filter( 
                Student.id == student_id 
                ).first() 
    if student is None: 
            raise HTTPException( 
                    status_code=404, 
                    detail="Student not found" 
                    ) 
    student.name = student_data.name 
    student.age = student_data.age 
    db.commit() 
    db.refresh(student) 
    return student


# DELETE: Delete a student

@router.delete("/{student_id}") 
def delete_student( 
        student_id: int, 
        db: Session = Depends(get_db)
        ):

    student = db.query(Student).filter( 
            Student.id == student_id ).first() 
    
    if student is None: 
        raise HTTPException( 
                status_code=404, 
                detail="Student not found" ) 
    db.delete(student) 
    db.commit() 
    return {"message": "Student deleted successfully", 
                "student_id": student_id }


#@router.patch("/{student_id}")

#def update_student_partial(

#        student_id: int,

#        student_data: StudentUpdate,

#        db: Session = Depends(get_db)

#        ):
