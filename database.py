import sqlite3
import datetime

class Database:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_table()
        self.insert_user("1", "1")
        self.insert_user("2", "2")

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY,
                                username TEXT NOT NULL,
                                password TEXT NOT NULL
                                )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tickets (
                                id INTEGER PRIMARY KEY,
                                ticket_number TEXT NOT NULL,
                                equipment TEXT NOT NULL,
                                fault_type TEXT NOT NULL,  -- Новое поле для типа неисправности
                                problem_description TEXT NOT NULL,
                                client TEXT NOT NULL,
                                status TEXT NOT NULL,
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                completion_date TIMESTAMP
                                )''')

    def insert_user(self, username, password):
        self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        self.conn.commit()

    def check_credentials(self, username, password):
        self.cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        return self.cursor.fetchone() is not None

    def insert_ticket(self, ticket_data):
        created_at = ticket_data.get('created_at', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.cursor.execute("INSERT INTO tickets (ticket_number, equipment, fault_type, problem_description, client, status, created_at, completion_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                        (ticket_data['ticket_number'], ticket_data['equipment'], ticket_data['fault_type'], ticket_data['problem_description'], ticket_data['client'], ticket_data['status'], created_at, ticket_data.get('completion_date', None)))
        self.conn.commit()


    def update_ticket(self, ticket_id, ticket_data):
        query = """
            UPDATE tickets
            SET equipment = ?,
                fault_type = ?,
                problem_description = ?,
                client = ?,
                status = ?,
                completion_date = ?
            WHERE id = ?
        """

    # Подготавливаем список значений для запроса
        values = [
            ticket_data.get('equipment', None),
            ticket_data.get('fault_type', None),  # Обновляем тип неисправности
            ticket_data.get('problem_description', None),
            ticket_data.get('client', None),
            ticket_data.get('status', None),
            ticket_data.get('completion_date', None),
            ticket_id
        ]

        self.cursor.execute(query, values)
        self.conn.commit()



    def delete_ticket(self, ticket_id):
        self.cursor.execute("DELETE FROM tickets WHERE id=?", (ticket_id,))
        self.conn.commit()

    def get_latest_ticket(self):
        self.cursor.execute("SELECT * FROM tickets ORDER BY id DESC LIMIT 1")
        return self.cursor.fetchone()

    def get_all_tickets(self):
        self.cursor.execute("SELECT * FROM tickets")
        return self.cursor.fetchall()

    def get_ticket_by_id(self, ticket_id):
        self.cursor.execute("SELECT * FROM tickets WHERE id=?", (ticket_id,))
        return self.cursor.fetchone()

    def search_tickets(self, query):
        self.cursor.execute("SELECT * FROM tickets WHERE ticket_number LIKE ? OR client LIKE ? OR equipment LIKE ?", ('%' + query + '%', '%' + query + '%', '%' + query + '%'))
        return self.cursor.fetchall()

    def __del__(self):
        self.conn.close()        