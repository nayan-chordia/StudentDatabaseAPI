from source.database import database_models
from source.schemas import data_schema


def insert_query(student: data_schema.Student):
    database_models.cursor.execute("""INSERT INTO students (age, first_name, family_name, gender, grade) VALUES (%s, %s, %s, %s, %s) RETURNING *""", 
                    (student.age, student.first_name, student.family_name, student.gender, student.grade))
    new_student = database_models.cursor.fetchone()
    database_models.conn.commit()
    return new_student


def select_query(id=None):
    if id == None:
        database_models.cursor.execute("""SELECT * FROM students ORDER BY id""")
        student = database_models.cursor.fetchall()
    else:
        database_models.cursor.execute("""SELECT * FROM students WHERE id = %s""", (str(id),))
        student = database_models.cursor.fetchone()
    return student


def update_query(id: int, updated_student: data_schema.Student, student: data_schema.Student):
    student = data_schema.Student(**student)
    updated_student = student.copy(update=updated_student.dict(exclude_unset=True))
    database_models.cursor.execute("""UPDATE students SET age = %s, First_Name = %s, Family_Name = %s, Gender = %s, Grade = %s WHERE id = %s RETURNING *""", 
                    (str(updated_student.age), updated_student.first_name, 
                        updated_student.family_name, updated_student.gender ,updated_student.grade, str(id)))
    database_models.conn.commit()
    updated_student = database_models.cursor.fetchone()
    return updated_student

def delete_query(id):
    database_models.cursor.execute("""DELETE FROM students WHERE id = %s RETURNING *""", (str(id),))
    deleted_student = database_models.cursor.fetchone()
    database_models.conn.commit()
    return deleted_student