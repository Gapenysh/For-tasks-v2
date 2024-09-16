# Создай метод для вывода данных


from mysql.connector import Error


class Users:

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
