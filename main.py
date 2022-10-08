from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time


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
                            id int NOT NULL PRIMARY KEY,
                            age int NOT NULL,
                            First_Name varchar(255) NOT NULL,
                            Family_Name varchar(255) NOT NULL,
                            Grade varchar NOT NULL
                        )"""
    cursor.execute(create_studentTable_query)
    conn.commit()

# cursor.execute("select * from information_schema.tables where table_name=%s", ('students',))
# print(bool(cursor.rowcount))


@app.get("/students")
def get_students():
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # return posts

    return {"message": "hi from nayan"}