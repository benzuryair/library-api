from database import db_connection
import logging


class SqlBooks:

    @staticmethod
    def create_book(data: dict):
        conn = db_connection.get_connection()
        cursor = conn.cursor()

        sql = """INSERT INTO books (title, author, genre) VALUES (%s, %s, %s);"""
        logging.info("The system was asked to add a book.")
        cursor.execute(sql, (data["title"], data["author"], data["genre"]))
        new_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        return new_id

    @staticmethod
    def get_all_books():
        conn = db_connection.get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = "select * from books"
        cursor.execute(sql)
        all_rows = cursor.fetchall()

        cursor.close()
        conn.close()
        return all_rows

    @staticmethod
    def get_book_by_id(id: int):
        conn = db_connection.get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = "select * from books where id =%s"

        cursor.execute(sql, (id,))
        one_line = cursor.fetchone()

        cursor.close()
        conn.close()

        return one_line

    @staticmethod
    def update_book(id: int, data: dict):
        conn = db_connection.get_connection()
        cursor = conn.cursor()

        set_parts = [f"{col}=%s" for col in data]
        set_clause = ", ".join(set_parts)

        values = list(data.values()) + [id]
        sql = f"update books set {set_clause} where id = %s"

        logging.info("The system was asked to update a book that exists in the table.")
        cursor.execute(sql, values)

        changed = cursor.rowcount > 0
        conn.commit()
        cursor.close()
        conn.close()
        return changed

    @staticmethod
    def set_available(id: int, val: bool, member_id: int):
        conn = db_connection.get_connection()
        cursor = conn.cursor()

        sql = "update books set is_available = %s, borrowed_by_member_id = %s where id = %s"
        logging.info("The system was asked to return/borrow a book.")
        cursor.execute(sql, (val, member_id, id))

        changed = cursor.rowcount > 0

        conn.commit()

        cursor.close()
        conn.close()

        return changed

    @staticmethod
    def count_total_books():
        conn = db_connection.get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = "SELECT COUNT(*) AS total_books FROM books"

        cursor.execute(sql)

        row = cursor.fetchone()

        cursor.close()
        conn.close()

        return row["total_books"]

    @staticmethod
    def count_available_books():
        conn = db_connection.get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = "SELECT COUNT(is_available) as available_books from books where is_available = True"

        cursor.execute(sql)
        row = cursor.fetchone()

        cursor.close()
        conn.close()

        return row["available_books"]

    @staticmethod
    def count_borrowed_books():
        conn = db_connection.get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = "SELECT COUNT(is_available) as borrowed_books from books where is_available = False"

        cursor.execute(sql)
        row = cursor.fetchone()

        cursor.close()
        conn.close()

        return row["borrowed_books"]

    @staticmethod
    def count_by_genre(genre: str):
        conn = db_connection.get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = "SELECT COUNT(genre) as sum_count_by_genre from books where genre = %s"

        cursor.execute(sql, (genre,))

        row = cursor.fetchone()

        cursor.close()
        conn.close()

        return row["sum_count_by_genre"]

    @staticmethod
    def count_active_borrows_by_member(member_id: int):
        conn = db_connection.get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = "SELECT COUNT(borrowed_by_member_id) as borrowed_member_books from books where borrowed_by_member_id = %s"

        cursor.execute(sql, (member_id,))

        row = cursor.fetchone()

        cursor.close()
        conn.close()

        return row["borrowed_member_books"]
