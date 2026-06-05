import sys,csv
from datetime import datetime
import sqlite3

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
                amount TEXT NOT NULL,
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
    def read_db(self):
        with self.get_connection() as conn:
            conn.execute("""SELECT * FROM expenses""")
            rows=conn.fetchall()
            print(rows)


def main():
    if len(sys.argv)==1:
        sys.exit("Send Request")
    elif sys.argv[1] in ['add','search','update']:
            pass
    else:
        raise ValueError("Invalid Request")

    db=ExpenseTracker()
    db.read_db()



def add_expense(db):
    t_types={1:"send",2:"recieve"}
    choice=int(input("TRANSACTION TYPE \n1-Send\n2-Recieve\n"))

    expense={
        "date": validate_date(input("DATE: ")),
        "amount":float(input("AMOUNT: ")),
        "t_type":t_types[choice],
        "note": input("NOTE: ")
    }
    
    db.add_expense(expense)
    

def write_expense(expense):
    conn=sqlite3.connect(db_name)
    cur=conn.cursor()

    cur.execute("""INSERT INTO expenses(
    date,amount,transaction_type,note) VALUES(?,?,?,?)""",(
        expense["date"],
        expense["amount"],
        expense["t_type"],
        expense["note"]

    ))
    conn.commit()
    conn.close()



def validate_date(inp_date):
    try:
        if "/" in inp_date:
            dt=datetime.strptime(inp_date, "%m/%d/%Y")
        else:
            dt=datetime.strptime(inp_date,"%B %d, %Y")
        return dt.strftime("%d-%m-%Y")
    except ValueError:
        print("invalid date format")

def search_expense():
    pass


def update_expense():
    pass


if __name__=='__main__':
    main()
