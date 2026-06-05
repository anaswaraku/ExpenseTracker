import sqlite3
from datetime import datetime
import calendar

class ExpenseTracker:
    """Class ExpenseTracker handle DB CRUD operations"""

    def __init__(self,db_name="expense.db"):
        self.db=db_name
        self.initialize_db()

    def get_connection(self):
        return sqlite3.connect(self.db)

    def initialize_db(self):
        with self.get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS expenses(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                transaction_type TEXT NOT NULL,
                note TEXT)""")

    def add_expense(self,expense):
        with self.get_connection() as conn:
            conn.execute("""INSERT INTO expenses(date,amount,transaction_type,note) VALUES(?,?,?,?)""",(
        expense["date"],
        expense["amount"],
        expense["t_type"],
        expense["note"]
    ))

    def read_all(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            query=("""SELECT * FROM expenses""")
            cursor.execute(query)
            rows=cursor.fetchall()
            print(rows)      

    def search_date(self,date):
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            query=("""SELECT * FROM expenses WHERE date=?""")
            cursor.execute(query,(date,))
            rows=cursor.fetchall()
            return rows

    def monthly_view(self, month_num):
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            query = """SELECT 
                COALESCE(SUM(CASE WHEN transaction_type='spent' THEN amount ELSE 0 END), 0) AS total_spent,
                COALESCE(SUM(CASE WHEN transaction_type='receive' THEN amount ELSE 0 END), 0) AS total_receive
                FROM expenses WHERE strftime('%m', date)=?"""
            cursor.execute(query, (f"{month_num:02d}",))
            row = cursor.fetchone()
            return dict(row) if row else {"total_spent": 0, "total_receive": 0}

    def monthly_report(self, month=None):
        with self.get_connection() as conn:
            if month:
                month_num = datetime.strptime(month, "%B").month
                return self.monthly_view(month_num)
            else:
                reports = []
                for i in range(1, 13):
                    reports.append(
                        {"month": calendar.month_name[i], "data": self.monthly_view(i)}
                    )
                return reports

    def deletetable(self):
        with self.get_connection() as conn:
            conn.execute("""DELETE FROM expenses""")
