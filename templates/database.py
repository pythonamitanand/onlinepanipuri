import mysql.connector
from datetime import datetime

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="db_panipuri"
        )
        self.cursor = self.conn.cursor(dictionary=True)
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INT AUTO_INCREMENT PRIMARY KEY,
                mobile VARCHAR(15) NOT NULL,
                address TEXT,
                plates INT NOT NULL,
                total_amount DECIMAL(10,2) NOT NULL,
                status ENUM('Pending', 'Completed') DEFAULT 'Pending',
                payment_status ENUM('Pending', 'Received') DEFAULT 'Pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS admin (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        """)
        self.conn.commit()

    def place_order(self, mobile, address, plates, total_amount):
        query = """
            INSERT INTO orders (mobile, address, plates, total_amount)
            VALUES (%s, %s, %s, %s)
        """
        self.cursor.execute(query, (mobile, address, plates, total_amount))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_orders(self):
        self.cursor.execute("SELECT * FROM orders ORDER BY created_at DESC")
        return self.cursor.fetchall()

    def update_order_status(self, order_id, status):
        query = "UPDATE orders SET status = %s WHERE id = %s"
        self.cursor.execute(query, (status, order_id))
        self.conn.commit()

    def update_payment_status(self, order_id, status):
        query = "UPDATE orders SET payment_status = %s WHERE id = %s"
        self.cursor.execute(query, (status, order_id))
        self.conn.commit()
