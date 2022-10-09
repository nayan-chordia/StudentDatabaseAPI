from fastapi import FastAPI, status, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from pydantic import BaseModel


class Student(BaseModel):
    age: int = None
    first_name: str = None
    family_name: str = None
    grade: str = None



app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='localhost',database='StudentDatabase',user='postgres', password='password1234', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection is successful")
        break
    except Exception as error:
        print("Connecting to databse failed")
        print("Error: ", error)
        time.sleep(2)


cursor.execute("select * from information_schema.tables where table_name=%s", ('students',))
if not bool(cursor.rowcount):
    create_studentTable_query = """CREATE TABLE students (
                            id serial NOT NULL PRIMARY KEY,
                            age int NOT NULL,
                            First_Name varchar(255) NOT NULL,
                            Family_Name varchar(255) NOT NULL,
                            Grade varchar NOT NULL
                        )"""
    cursor.execute(create_studentTable_query)
    conn.commit()


# Add new Students

@app.post("/students", status_code=status.HTTP_201_CREATED)
def add_students(student: Student):
    cursor.execute("""INSERT INTO students (age, first_name, family_name, grade) VALUES (%s, %s, %s, %s) RETURNING *""", 
                    (student.age, student.first_name, student.family_name, student.grade))
    new_student = cursor.fetchone()
    conn.commit()
    return new_student

# Get all students

@app.get("/students")
def get_students():
    cursor.execute("""SELECT * FROM students""")
    students = cursor.fetchall()
    return students

# Get student by id

@app.get("/students/{id}")
def get_students(id):
    cursor.execute("""SELECT * FROM students WHERE id = %s""", (str(id)))
    student = cursor.fetchone()
    return student

# Update Student

@app.patch("/students/{id}")
def update_student(id: int, updated_student: Student):

    cursor.execute("""SELECT * FROM students WHERE id = %s""", (str(id)))
    student = cursor.fetchone()

    if student == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"student with {id} was not found")

    student = Student(**student)
    updated_student = student.copy(update=updated_student.dict(exclude_unset=True))
    print(updated_student)
    cursor.execute("""UPDATE students SET age = %s, First_Name = %s, Family_Name = %s, Grade = %s WHERE id = %s RETURNING *""", 
                    (str(updated_student.age), updated_student.first_name, 
                        updated_student.family_name, updated_student.grade, str(id)))

    updated_student = cursor.fetchone()
    conn.commit()

    return updated_student