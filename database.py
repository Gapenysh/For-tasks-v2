from users.view import router as users_router
from fastapi import FastAPI
from mysql.connector import connect
import os
from dotenv import load_dotenv
import pymysql

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
