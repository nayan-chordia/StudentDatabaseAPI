import time
import psycopg2
from psycopg2.extras import RealDictCursor
from configuration.config import settings

host = settings.database_hostname
db = settings.database_name
username = settings.database_username
pwd = settings.database_password

while True:
    try:
        conn = psycopg2.connect(host=host,database=db,user=username, password=pwd, cursor_factory=RealDictCursor)
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
                            Gender varchar NOT NULL,
                            Grade varchar NOT NULL
                        )"""
    cursor.execute(create_studentTable_query)
    conn.commit()