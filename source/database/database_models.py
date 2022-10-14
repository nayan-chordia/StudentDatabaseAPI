from configuration.config import settings
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from source.database.database_helper import conn, cursor

host = settings.database_hostname
db = settings.database_name
username = settings.database_username
pwd = settings.database_password


def create_database():
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor.execute("CREATE DATABASE "+ str(db))
    print('StudentDatabse created')


def create_table():
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


# This checks if we have already created database or not
cursor.execute("""SELECT datname FROM pg_catalog.pg_database WHERE lower(datname) = lower('studentdatabase')""")
if not bool(cursor.rowcount):
    create_database()

# This checks if we have already created table or not
cursor.execute("select * from information_schema.tables where table_name=%s", ('students',))
if not bool(cursor.rowcount):
    create_table()