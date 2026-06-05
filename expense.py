import sqlite3
from datetime import datetime

class ExpenseTracker:
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
            query=("""DELETE FROM expenses""")
            cursor.execute(query)
            rows=cursor.fetchall()
            print(rows)      

    def search_date(self,date):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            query=("""SELECT * FROM expenses WHERE date=?""")
            cursor.execute(query,(date,))
            rows=cursor.fetchall()
            print(rows)

    def monthly_report(self,month):
        with self.get_connection() as conn:
            cursor=conn.cursor()
            month_num=datetime.strptime(month,"%B").month
            
            query="""SELECT SUM(CASE 
            WHEN transaction_type='spent' THEN amount ELSE 0 END) AS total_spent FROM expenses WHERE strftime('%m',date)=?"""
            cursor.execute(query,(f"{month_num:02d}",))
            rows=cursor.fetchone()
            print(rows)#type: list
            return rows
    def deletetable(self):
        with self.get_connection() as conn:
            conn.execute("""DELETE FROM expenses""")
           
            
        

