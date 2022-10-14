import time
import psycopg2
from configuration.config import settings
from psycopg2.extras import RealDictCursor

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
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)