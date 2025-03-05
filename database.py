from mysql.connector import connect


username = "zilant"
password = "111111"
hostname = "192.168.88.81"
databasename = "v2_tasks_db"


class DataBaseConn:
    def __init__(self):
        self.connection = connect(
            host=hostname,
            user=username,
            password=password,
            database=databasename,
        )
