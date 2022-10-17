from fastapi import HTTPException, status
from source.schemas import data_schema
from source.queries import students_queries
from source.exceptions.service_exceptions import HTTPExceptionHandler


def add_students(student: data_schema.Student):
    new_student = students_queries.insert_query(student)
    return new_student


def get_students():
    students = students_queries.select_query()
    return students


def get_student_by_id(id):
    student = students_queries.select_query(id)
    if student == None:
        raise HTTPExceptionHandler(id=id)    
    return student


def update_student(id: int, updated_student: data_schema.Student):
    student = students_queries.select_query(id)
    if student == None:
        raise HTTPExceptionHandler(id=id) 
    updated_student = students_queries.update_query(id,updated_student, student)
    return updated_student


def delete_student(id: int):
    deleted_student = students_queries.delete_query(id)
    if deleted_student == None:
        raise HTTPExceptionHandler(id=id) 
    return deleted_student