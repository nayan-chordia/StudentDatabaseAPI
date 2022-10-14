from fastapi import HTTPException, status
from source.database import database_models
from source.schemas import data_schema
from source.queries import students_queries


def add_students(student: data_schema.Student):
    new_student = students_queries.insert_query(student)
    return new_student


def get_students():
    students = students_queries.select_query()
    return students


def get_student_by_id(id):
    student = students_queries.select_query(id)
    if student == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"student with {id} was not found")
    
    return student


def update_student(id: int, updated_student: data_schema.Student):
    student = students_queries.select_query(id)
    if student == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"student with {id} was not found")
    updated_student = students_queries.update_query(id,updated_student, student)
    return updated_student


def delete_student(id: int):
    deleted_student = students_queries.delete_query(id)
    if deleted_student == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"student with {id} was not found")
    return deleted_student