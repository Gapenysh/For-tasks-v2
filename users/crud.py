# Создай метод для вывода данных


from mysql.connector import Error


class Users:

    @staticmethod
    def exist_user_id(id):
        from database import DataBaseConn

        try:
            conn = DataBaseConn().connection
            cur = conn.cursor()
            stmt_check_user = """SELECT COUNT(*) FROM tasks WHERE id = %s"""
            cur.execute(stmt_check_user, (id,))
            user_exists = cur.fetchone()[0]

            if user_exists == 0:
                print(f"Пользователь с id = {id} не найден")
                return None
            else:
                return True
        except Error as e:
            print("Ошибка получения доступа к БД: " + str(e))
            return None

    @staticmethod
    def get_users():
        from database import DataBaseConn

        try:
            conn = DataBaseConn().connection
            cursor = conn.cursor()
            stmt = """SELECT * FROM users"""
            cursor.execute(stmt)
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            return result
        except Error as e:
            return str(e)

    # Добавить проверку на оригинальность имени
    @staticmethod
    def add_user(username: str):
        from database import DataBaseConn

        try:
            conn = DataBaseConn().connection
            cursor = conn.cursor()

            stmt = f"""INSERT INTO users (username) VALUES(%s)"""
            cursor.execute(stmt, (username,))
            conn.commit()
            print("add_user done successfully")
            cursor.close()
            conn.close()
            return True
        except Error as e:
            print(str(e))
            return None

    @staticmethod
    def delete_user(id):
        from database import DataBaseConn

        try:
            exist_user = Users.exist_user_id(id)
            if exist_user is None:
                return None
            conn = DataBaseConn().connection
            cur = conn.cursor()
            stmt_task_users = """DELETE FROM task_users WHERE user_id = %s"""
            stmt_users = """DELETE FROM users WHERE id = %s"""

            cur.execute(stmt_task_users, (id,))
            cur.execute(stmt_users, (id,))

            conn.commit()
            cur.close()
            conn.close()
            return True
        except Error as e:
            print("Ошибка с подключением к БД" + str(e))
            return None
