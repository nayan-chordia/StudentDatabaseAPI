from fastapi import FastAPI, status, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from pydantic import BaseModel


class Student(BaseModel):
    age: int
    first_name: str
    family_name: str
    grade: str



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


@app.get("/students")
def get_students():
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # return posts

    return {"message": "hi from nayan"}