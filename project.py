import sys,csv
from datetime import datetime,date
import sqlite3
from expense import ExpenseTracker

def main():
    # if len(sys.argv)==1:
    #     sys.exit("Send Request")
    # elif sys.argv[1] in ['add','search','report']:
    #         pass
    # else:
    #     raise ValueError("Invalid Request")

    db=ExpenseTracker()
    #add_expense(db)

    if sys.argv[1]=='add':
        add_expense(db)
    elif sys.argv[1]=='search':
        db.read_all()
    elif sys.argv[1]=='report':
        db.monthly_report('January')
    else:
        db.deletetable()



def add_expense(db):
    t_types={1:"spent",2:"recieve"}
    choice=int(input("TRANSACTION TYPE \n1-Spend\n2-Recieve\n"))

    expense={
        "date": validate_date(input("DATE: ")),
        "amount":float(input("AMOUNT: ")),
        "t_type":t_types[choice],
        "note": input("NOTE: ")
    }
    
    db.add_expense(expense)
    

def validate_date(inp_date):
    try:
        if "/" in inp_date:
            dt=datetime.strptime(inp_date, "%d/%m/%Y")
        else:
            dt=datetime.strptime(inp_date,"%B %d, %Y")
        return dt.date().isoformat()
    except ValueError:
        return None

def search_expense():
    pass


def update_expense():
    pass


if __name__=='__main__':
    main()
