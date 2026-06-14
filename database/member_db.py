import logging
from database import db_connection


class SqlMember:

    @staticmethod
    def create_member(data: dict):
        conn = db_connection.get_connection()
        cursor = conn.cursor()

        sql = "insert into membrs(name, email, is_active, total_borrows) values(%s, %s, %s, %s)"

        values = list(data.values())
        logging.info("The system was asked to create a new member for the library.")
        cursor.execute(sql, values)

        new_id = cursor.lastrowid

        conn.commit()

        cursor.close()
        conn.close()

        return new_id

    @staticmethod
    def get_all_members():
        conn = db_connection.get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = "select * from members"

        cursor.execute(sql)

        cursor.close()
        conn.close()

        rows = cursor.fetchall()

        return rows

    @staticmethod
    def get_member_by_id(id: int):
        conn = db_connection.get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = "select * from members where id = %s"

        cursor.execute(sql, (id,))

        row = cursor.fetchone()

        cursor.close()
        conn.close()

        return row

    @staticmethod
    def update_member(id: int, data: dict):
        conn = db_connection.get_connection()
        cursor = conn.cursor()

        list_of_keys = [f"{col}=%s" for col in data]
        join_list = ", ".join(list_of_keys)

        values = list(data.values()) + [id]

        logging.info("The system was asked to update the details of a library member.")
        sql = f"update members set {join_list} where id = %s"

        cursor.execute(sql, values)

        changed = cursor.rowcount > 0

        conn.commit()

        cursor.close()
        conn.close()

        return changed

    @staticmethod
    def deactivate_member(id: int):
        conn = db_connection.get_connection()
        cursor = conn.cursor()

        logging.info("The system was asked to deactivate a library member.")
        sql = "update members set is_active = False where id = %s"

        cursor.execute(sql, (id,))

        changed = cursor.rowcount > 0

        conn.commit()
        cursor.close()
        conn.close()

        return changed

    @staticmethod
    def activate_member(id: int):
        conn = db_connection.get_connection()
        cursor = conn.cursor()

        logging.info("The system was asked to activate a library member.")
        sql = "update members set is_active = True where id = %s"

        cursor.execute(sql, (id,))

        changed = cursor.rowcount > 0

        conn.commit()
        cursor.close()
        conn.close()

        return changed

    @staticmethod
    def increment_borrows(id: int):
        conn = db_connection.get_connection()
        cursor = conn.cursor()

        logging.info("The system was asked to add another loan to the number of loans.")
        sql = "update members set total_borrows = total_borrows + 1 where id = %s"

        cursor.execute(sql, (id,))

        changed = cursor.rowcount > 0

        conn.commit()
        cursor.close()
        conn.close()

        return changed

    @staticmethod
    def count_active_members():
        conn = db_connection.get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = "select count(is_active) as active_members from members where is_active = True "

        cursor.execute(sql)

        row = cursor.fetchone()

        cursor.close()
        conn.close()

        return row["active_members"]

    @staticmethod
    def get_top_member():
        conn = db_connection.get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = "SELECT MAX(total_borrows) as top_member from members "

        cursor.execute(sql)

        row = cursor.fetchone()

        cursor.close()
        conn.close()

        return row["top_member"]
