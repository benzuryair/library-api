import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host="localhost", port=3306, user="root", password="root", database="library_db"
    )


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    sql1 = """CREATE TABLE IF NOT EXISTS books(
            id INT PRIMARY KEY AUTO_INCREMENT,
            title VARCHAR(50) NOT NULL,
            author VARCHAR(50) NOT NULL,
            genre ENUM('Fiction', 'Non-Fiction', 'Science', 'History', 'Other') NOT NULL,
            is_available BOOLEAN DEFAULT TRUE NOT NULL,
            borrowed_by_member_id INT
        )"""

    sql2 = """CREATE TABLE IF NOT EXISTS members(
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(50) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        is_active BOOLEAN DEFAULT TRUE NOT NULL,
        total_borrows INT DEFAULT 0
    )"""
    cursor.execute(sql1)
    cursor.execute(sql2)
    conn.commit()
    cursor.close()
    conn.close()
