import sqlite3
from datetime import datetime
import calendar


class ExpenseTracker:
    """Class ExpenseTracker handle DB CRUD operations"""

    def __init__(self, db_name="expense.db"):
        self.db = db_name
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
                note TEXT,
                category TEXT)""")
            try:
                conn.execute("SELECT category FROM expenses LIMIT 1")
            except sqlite3.OperationalError:
                conn.execute("ALTER TABLE expenses ADD COLUMN category TEXT")

    def add_expense(self, expense):
        with self.get_connection() as conn:
            conn.execute(
                """INSERT INTO expenses(date,amount,transaction_type,note,category) VALUES(?,?,?,?,?)""",
                (
                    expense["date"],
                    expense["amount"],
                    expense["t_type"],
                    expense["note"],
                    expense["category"],
                ),
            )

    def read_all(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            query = """SELECT * FROM expenses ORDER BY date, id"""
            cursor.execute(query)
            rows = cursor.fetchall()
            print(rows)

    def search_date(self, date):
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            query = """SELECT * FROM expenses WHERE date=? ORDER BY id"""
            cursor.execute(query, (date,))
            rows = cursor.fetchall()
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

    def get_category_report_for_month(self, month_num):
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            query = """SELECT
                category,
                COALESCE(SUM(amount), 0) as total_spent
                FROM expenses
                WHERE strftime('%m', date) = ? AND transaction_type = 'spent'
                GROUP BY category
                ORDER BY total_spent DESC"""
            cursor.execute(query, (f"{month_num:02d}",))
            return cursor.fetchall()

    def get_transactions_for_month(self, month_num):
        """Fetches all transactions for a given month number."""
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            query = """SELECT date, amount, transaction_type, note, category
                       FROM expenses
                       WHERE strftime('%m', date) = ?
                       ORDER BY date, id"""
            cursor.execute(query, (f"{month_num:02d}",))
            return cursor.fetchall()

    def get_balance_up_to_date(self, date):
        """Calculates the total balance up to (but not including) a specific date."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            query = """SELECT
                COALESCE(SUM(CASE
                    WHEN transaction_type='receive' THEN amount
                    WHEN transaction_type='spent' THEN -amount
                    ELSE 0 END), 0) as balance
                FROM expenses WHERE date < ?"""
            cursor.execute(query, (date,))
            result = cursor.fetchone()
            return result[0] if result else 0

    def monthly_report(self, month=None):
        if month:
            try:
                month_num = datetime.strptime(month, "%B").month
                return self.monthly_view(month_num)
            except ValueError:
                return None
        else:
            with self.get_connection() as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                query = """
                    SELECT
                        strftime('%m', date) AS month_num_str,
                        COALESCE(SUM(CASE WHEN transaction_type = 'spent' THEN amount ELSE 0 END), 0) AS total_spent,
                        COALESCE(SUM(CASE WHEN transaction_type = 'receive' THEN amount ELSE 0 END), 0) AS total_receive
                    FROM expenses
                    GROUP BY month_num_str
                    ORDER BY month_num_str
                """
                cursor.execute(query)
                db_rows = cursor.fetchall()

                reports = []
                for row in db_rows:
                    month_num = int(row["month_num_str"])
                    reports.append(
                        {
                            "month": calendar.month_name[month_num],
                            "data": {
                                "total_spent": row["total_spent"],
                                "total_receive": row["total_receive"],
                            },
                        }
                    )
                return reports

    def deletetable(self):
        with self.get_connection() as conn:
            conn.execute("""DELETE FROM expenses""")
