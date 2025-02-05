from mysql.connector import connect
import os
from dotenv import load_dotenv


origins = [
    "http://localhost:4200",
]

load_dotenv()

username = "root"
password = os.getenv("PASSWORD")
hostname = os.getenv("HOSTNAME")
databasename = os.getenv("DATABASENAME")


print(username)
print(password)
print(hostname)
print(databasename)


class DataBaseConn:
    def __init__(self):
        self.connection = connect(
            host=hostname,
            user=username,
            password=password,
            database=databasename,
        )
