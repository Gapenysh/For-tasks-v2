# Создай метод для вывода данных
import datetime

from mysql.connector import Error
from database import DataBaseConn
from .schemas import Task


class Tasks:

    @staticmethod
    def get_tasks():

        try:
            conn = DataBaseConn().connection
            cur = conn.cursor()
            stmt = """SELECT tasks.title, 
            tasks.detail, 
            tasks.creation_date, 
            tasks.execution_date, 
            tasks.execution_mark,
            GROUP_CONCAT(users.username ORDER BY users.username SEPARATOR ', ') AS executors
            FROM task_users tu
            INNER JOIN 
            tasks ON tu.task_id = tasks.id
            INNER JOIN 
            users ON tu.user_id = users.id
            GROUP BY tu.task_id"""
            cur.execute(stmt)
            result = cur.fetchall()
            print("get_tasks(показ задач) сработал корректно")
            return result
        except Error as e:
            return str(e)

    @staticmethod
    def get_task_by_id(task_id: int):
        try:
            conn = DataBaseConn().connection
            cur = conn.cursor()
            stmt = """SELECT tasks.title, 
            tasks.detail, 
            tasks.creation_date, 
            tasks.execution_date, 
            tasks.execution_mark,
            GROUP_CONCAT(users.username ORDER BY users.username SEPARATOR ', ') AS executors
            FROM task_users tu
            INNER JOIN 
            tasks ON tu.task_id = tasks.id
            INNER JOIN 
            users ON tu.user_id = users.id
            WHERE tasks.id = %s
            GROUP BY tu.task_id"""
            cur.execute(stmt, (task_id,))
            result = cur.fetchone()

            cur.close()
            conn.close()
            return result
        except Error as e:
            return str(e)

    @staticmethod
    def create_task(
        title: str,
        detail: str,
        creat_date: str,
        exec_date: str,
        exec_mark: str,
        executors: list[int],
    ):
        try:
            conn = DataBaseConn().connection
            cur = conn.cursor()
            stmt_tasks = """INSERT INTO tasks (title, detail, creation_date, execution_date, execution_mark) VALUES(%s, %s, %s, %s, %s)"""
            tasks_value = (
                title,
                detail,
                creat_date,
                exec_date,
                exec_mark,
            )
            cur.execute(stmt_tasks, tasks_value)
            task_id = cur.lastrowid

            # add loop for creating task
            if executors:
                for executor_id in executors:
                    stmt_task_users = (
                        """INSERT INTO task_users (task_id, user_id) VALUES(%s, %s)"""
                    )
                    task_user_value = (task_id, executor_id)
                    cur.execute(stmt_task_users, task_user_value)
            conn.commit()
            cur.close()
            conn.close()
            print("add_task(добавление задачи) сработал корректно")
            return True
        except Error as e:
            print("Ошибка получения доступа к БД: " + str(e))
            return None

    @staticmethod
    def update_task(id, title, detail, creat_date, exec_date, mark):
        pass
        try:
            conn = DataBaseConn().connection
            cur = conn.cursor()
            stmt = """UPDATE tasks
            SET title = %s
            detail = %s
            creation_date = %s
            execution_date = %s
            execution_mark = %s
            """
            values = (title, detail, creat_date, exec_date, mark, id)
            cur.execute(stmt, values)
            conn.commit()
            cur.close()
            conn.close()
            print("Обновление задачи прошло успешно")
            return True
        except Error as e:
            print("Ошибка обновления задачи: " + str(e))
            return False
