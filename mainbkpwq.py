






#from fastapi import FastAPI, Depends, HTTPException

#from sqlalchemy.orm import Session

#from pydantic import BaseModel, Field



#from db import get_db

#from models import Student

#from routers.students import router as students_router

#app = FastAPI(title="Student Management API")


#class StudentCreate(BaseModel):

#     name: str = Field(min_length=1, max_length=100)
 
#     age: int = Field(gt=0)



#@app.get("/")

#def home():

#       return {"message": "Student Management API is running"}

#@app.include_router(students_router)


 
#@app.post("/students/")

#def create_student(

#    student: StudentCreate,

#    db: Session = Depends(get_db)

#):

#    new_student = Student(name=student.name, age=student.age)

#    db.add(new_student)

#    db.commit()

#    db.refresh(new_student)

#    return {

#        "id": new_student.id,

#        "name": new_student.name,

#        "age": new_student.age

#     }




 
#@app.get("/students/")

#def get_students(db: Session = Depends(get_db)):

#    return db.query(Student).order_by(Student.id).all()




#@app.get("/students/{student_id}")

#def get_student(student_id: int, db: Session = Depends(get_db)):
#         student = db.query(Student).filter(
#             Student.id == student_id
#         ).first()

#         if student is None:
#             raise HTTPException(status_code=404, detail="Student not found")

#         return student
# UPDATE: Update a student's name and age 
#@app.put("/students/{student_id}") 
#def update_student( 
#        student_id: int, 
#        student_data: StudentCreate, 
#        db: Session = Depends(get_db) 
#): 
#    student = db.query(Student).filter( 
#            Student.id == student_id 
#            ).first()
#    print (student)

#    if student is None: 
#        raise HTTPException( 
#                status_code=404, 
#                detail="Student not found" ) 
#    student.name = student_data.name 
#    student.age = student_data.age  
#    db.commit() 
#    db.refresh(student) 
#    return student 
# DELETE: Remove a student by ID 
#@app.delete("/students/{student_id}") 
#def delete_student( 
#        student_id: int,
#        db: Session = Depends(get_db) ): 
#    student = db.query(Student).filter( 
#            Student.id == student_id ).first() 
#    if student is None: 
#        raise HTTPException(
#                status_code=404,
#                detail="Student not found" )
#        db.delete(student)
#        db.commit() 
#        return { "message": "Student deleted successfully", "student_id": student_id }
#                
#
 #                                   
#
#
#
#
#                                   
