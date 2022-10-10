from fastapi import APIRouter, status
from ..schemas import data_schema
from ..services import students_services

router = APIRouter()

# Add new Students

@router.post("/students", status_code=status.HTTP_201_CREATED)
def add_students(student: data_schema.Student):
    return students_services.add_students(student)


# Get all students

@router.get("/students")
def get_students():
    return students_services.get_students()


# Get student by id

@router.get("/students/{id}")
def get_students(id):
    return students_services.get_student_by_id(id)

# Update Student

@router.patch("/students/{id}")
def update_student(id: int, updated_student: data_schema.Student):
    return students_services.update_student(id,updated_student)


# Delete student by id

@router.delete("/students/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(id: int):
    return students_services.delete_student(id)