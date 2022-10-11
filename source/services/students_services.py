from fastapi import HTTPException, status
from source.database import database_models
from source.schemas import data_schema


def add_students(student: data_schema.Student):
    database_models.cursor.execute("""INSERT INTO students (age, first_name, family_name, gender, grade) VALUES (%s, %s, %s, %s, %s) RETURNING *""", 
                    (student.age, student.first_name, student.family_name, student.gender, student.grade))
    new_student = database_models.cursor.fetchone()
    database_models.conn.commit()
    return new_student


def get_students():
    database_models.cursor.execute("""SELECT * FROM students""")
    students = database_models.cursor.fetchall()
    return students


def get_student_by_id(id):
    database_models.cursor.execute("""SELECT * FROM students WHERE id = %s""", (str(id),))
    student = database_models.cursor.fetchone()
    if student == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"student with {id} was not found")
    
    return student


def update_student(id: int, updated_student: data_schema.Student):
    database_models.cursor.execute("""SELECT * FROM students WHERE id = %s""", (str(id),))
    student = database_models.cursor.fetchone()

    if student == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"student with {id} was not found")

    student = data_schema.Student(**student)
    updated_student = student.copy(update=updated_student.dict(exclude_unset=True))
    database_models.cursor.execute("""UPDATE students SET age = %s, First_Name = %s, Family_Name = %s, Gender = %s, Grade = %s WHERE id = %s RETURNING *""", 
                    (str(updated_student.age), updated_student.first_name, 
                        updated_student.family_name, updated_student.gender ,updated_student.grade, str(id)))

    updated_student = database_models.cursor.fetchone()
    database_models.conn.commit()

    return updated_student


def delete_student(id: int):
    database_models.cursor.execute("""DELETE FROM students WHERE id = %s RETURNING *""", (str(id),))
    deleted_student = database_models.cursor.fetchone()

    if deleted_student == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"student with {id} was not found")

    database_models.conn.commit()
    return deleted_student