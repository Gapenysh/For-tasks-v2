# Создай метод для вывода данных
import datetime
from typing import List

from mysql.connector import Error
from database import DataBaseConn


class Tasks:

    @staticmethod
    def exist_task_id(id):
        try:
            conn = DataBaseConn().connection
            cur = conn.cursor()
            stmt_check_user = """SELECT COUNT(*) FROM tasks WHERE id = %s"""
            cur.execute(stmt_check_user, (id,))
            user_exists = cur.fetchone()[0]

            if user_exists == 0:
                print(f"Задача c id = {id} не найдена")
                return None
            else:
                return True
        except Error as e:
            print("Ошибка получения доступа к БД: " + str(e))
            return None

    @staticmethod
    def get_tasks():

        try:
            conn = DataBaseConn().connection
            cur = conn.cursor()
            stmt = """SELECT tasks.id,
            tasks.title, 
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
            stmt = """SELECT tasks.id,
            tasks.title, 
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
    def get_users_from_task_id(id: int):
        try:
            conn = DataBaseConn().connection
            cur = conn.cursor()
            stmt = """SELECT id, username FROM users
                    INNER JOIN task_users ON users.id = task_users.user_id
                    WHERE task_users.task_id = %s"""
            cur.execute(stmt, (id,))
            result = cur.fetchall()
            print("Исполнители из задачи id = {id} были отправлены")
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
        try:
            conn = DataBaseConn().connection
            cur = conn.cursor()
            stmt = """UPDATE tasks
            SET title = %s,
            detail = %s,
            creation_date = %s,
            execution_date = %s,
            execution_mark = %s
            WHERE tasks.id = %s
            """
            values = (title, detail, creat_date, exec_date, mark, id)
            print(type(values))
            cur.execute(stmt, values)
            conn.commit()
            cur.close()
            conn.close()
            print("Обновление задачи прошло успешно")
            return True
        except Error as e:
            print("Ошибка обновления задачи: " + str(e))
            return False

    @staticmethod
    def update_task_status(id, status):
        try:
            exist = Tasks.exist_task_id(id)
            if exist is None:
                return False
            conn = DataBaseConn().connection
            cur = conn.cursor()

            stmt = """UPDATE tasks
            SET execution_mark = %s
            WHERE id = %s"""
            values = (status, id)
            cur.execute(stmt, values)
            conn.commit()
            cur.close()
            conn.close()
            print("Обновление статуса задачи прошло успешно")
            return True
        except Error as e:
            print("Ошибка обновления задачи: " + str(e))
            return False

    @staticmethod
    def update_task_executors(id, executors):
        try:
            exist = Tasks.exist_task_id(id)
            if exist is None:
                return False
            conn = DataBaseConn().connection
            cur = conn.cursor()
            delete_stmt = """DELETE FROM task_users WHERE task_id = %s"""
            cur.execute(delete_stmt, (id,))
            if executors:
                for executor_id in executors:
                    stmt_task_users = (
                        """INSERT INTO task_users (task_id, user_id) VALUES(%s, %s)"""
                    )
                    task_user_value = (id, executor_id)
                    cur.execute(stmt_task_users, task_user_value)

            conn.commit()
            cur.close()
            conn.close()
            print(f"Обновление пользлвателей для задачи {id} прошло успешно")
            return True
        except Error as e:
            print("Ошибка обновления задачи: " + str(e))
            return False

    @staticmethod
    def get_info_by_status(status):

        valid_status = {
            "status2": "В работе",
            "status3": "Готово",
        }

        if status not in valid_status:
            raise ValueError("Invalid status")

        status = valid_status[status]
        print(status)
        try:
            connection = DataBaseConn().connection
            cursor = connection.cursor()
            query = """SELECT tasks.id,
            tasks.title, 
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
            WHERE tasks.execution_mark = %s
            GROUP BY tu.task_id"""

            cursor.execute(query, (status,))

            data = cursor.fetchall()
            cursor.close()
            connection.close()
            print("get_info_by_status сработал")
            return data
        except Error as e:
            return str(e)

    @staticmethod
    def delete_task(id):
        try:
            exist_task = Tasks.exist_task_id(id)
            if exist_task is None:
                return None
            conn = DataBaseConn().connection
            cur = conn.cursor()
            stmt_task_users = """DELETE FROM task_users WHERE task_id = %s"""
            stmt_tasks = """DELETE FROM tasks WHERE id = %s"""

            cur.execute(stmt_task_users, (id,))
            cur.execute(stmt_tasks, (id,))

            conn.commit()
            cur.close()
            conn.close()
            print("Удаление задачи сработало корректно")
            return True
        except Error as e:
            print("Ошибка удаление задачи: " + str(e))
            return None

    @staticmethod
    def filter_from_users(executors_id: List[int]):
        try:
            conn = DataBaseConn().connection
            cur = conn.cursor()
            placeholders = ", ".join(["%s"] * len(executors_id))
            stmt = f"""SELECT tasks.id,
            tasks.title,
            tasks.detail,
            tasks.creation_date,
            tasks.execution_date,
            tasks.execution_mark,
            GROUP_CONCAT(users.username ORDER BY users.username 
            ) AS executors
            FROM task_users tu
            INNER JOIN tasks ON tu.task_id = tasks.id
            INNER JOIN users ON tu.user_id = users.id
            WHERE tasks.id IN (
                SELECT DISTINCT tu.task_id
                FROM task_users tu
                WHERE tu.user_id IN ({placeholders})
            )
            GROUP BY tasks.id
        """
            cur.execute(stmt, executors_id)
            result = cur.fetchall()
            print("filter_by_users сработал корректно")
            return result
        except Error as e:
            return str(e)

    @staticmethod
    def search_tasks_by_query(query: str):
        try:
            conn = DataBaseConn().connection
            cur = conn.cursor()
            stmt = """SELECT tasks.id,
            tasks.title, 
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
            WHERE MATCH(tasks.title) AGAINST(%s IN NATURAL LANGUAGE MODE)
            GROUP BY tasks.id
            """
            cur.execute(stmt, (query,))
            tasks = cur.fetchall()
            return tasks
        except Error as e:
            return str(e)

    @staticmethod
    def filter_from_users_status(status: str, executors_id: List[int]):
        valid_status = {
            "status1": "В очереди",
            "status2": "В работе",
            "status3": "Готово",
        }

        if status not in valid_status:
            raise ValueError("Invalid status")

        mark = valid_status[status]
        try:
            conn = DataBaseConn().connection
            cur = conn.cursor()
            placeholders = ", ".join(["%s"] * len(executors_id))

            stmt = f"""SELECT tasks.id, tasks.title, tasks.detail, tasks.creation_date, tasks.execution_date, tasks.execution_mark,
            GROUP_CONCAT(users.username ORDER BY users.username) AS executors
            FROM task_users tu
            INNER JOIN tasks ON tu.task_id = tasks.id
            INNER JOIN users ON tu.user_id = users.id
            WHERE tasks.id IN (
                SELECT DISTINCT tu.task_id
                FROM task_users tu
                WHERE tu.user_id IN ({placeholders})
            )
            GROUP BY tasks.id
            HAVING tasks.execution_mark = %s"""
            cur.execute(stmt, executors_id + [mark])
            tasks_filter_status_users = cur.fetchall()
            return tasks_filter_status_users
        except Error as e:

            return str(e)

    @staticmethod
    def get_all_tasks_for_user(user_id: int):

        try:
            conn = DataBaseConn().connection
            cur = conn.cursor()
            stmt = f"""SELECT tasks.id, tasks.title, tasks.detail, tasks.creation_date, tasks.execution_date, tasks.execution_mark,
                        GROUP_CONCAT(users.username ORDER BY users.username) AS executors
                        FROM task_users tu
                        INNER JOIN tasks ON tu.task_id = tasks.id
                        INNER JOIN users ON tu.user_id = users.id
                        WHERE tasks.id IN (
                            SELECT DISTINCT tu.task_id
                            FROM task_users tu
                            WHERE tu.user_id IN (%s)
                        )
                        GROUP BY tasks.id
                        HAVING tasks.execution_mark NOT IN ("Готово")"""
            cur.execute(stmt, (user_id,))
            tasks_for_users = cur.fetchall()

            return tasks_for_users

        except Error as e:
            print(str(e))
            return None
