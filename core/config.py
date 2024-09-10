from mysql.connector import connect
import os
from dotenv import load_dotenv


origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://example.com",
]

load_dotenv()

username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
hostname = os.getenv("HOSTNAME")
databasename = os.getenv("DATABASENAME")


class DataBaseConn:
    def __init__(self):
        self.connection = connect(
            host=hostname,
            user=username,
            password=password,
            database=databasename,
        )
