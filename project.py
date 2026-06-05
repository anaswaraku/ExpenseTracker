import sys,csv
from datetime import datetime
import sqlite3

db_name="expense.db"

def main():

    if len(sys.argv)==1:
        sys.exit("Send Request")
    elif sys.argv[1] in ['add','search','update']:
            pass
    else:
        raise ValueError("Invalid Request")

    request_map={
        "add": add_expense}

    request_map[sys.argv[1]]()

def initialize_db():
    conn=sqlite3.connect(db_name)
    cur=conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS expenses(
    id INTEGER PRIMARY KEY AUTOINCREMENT.
    date TEXT NOT NULL,
    amount TEXT NOT NULL,
    transaction_type TEXT NOT NULL,
    note TEXT)""")

    conn.commit()
    conn.close()

def add_expense():
    t_types={1:"send",2:"recieve"}
    choice=int(input("TRANSACTION TYPE \n1-Send\n2-Recieve\n"))

    expense={
        "date": validate_date(input("DATE: ")),
        "amount":float(input("AMOUNT: ")),
        "t_type":t_types[choice],
        "note": input("NOTE: ")
    }
    try:
        write_expense(expense)
    except:
        sys.exit("Adding Failed")
    else:
        sys.exit("Added Successfully")
    

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
