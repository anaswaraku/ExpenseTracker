import sys,csv
from datetime import datetime,date
import sqlite3
from expense import ExpenseTracker
from fpdf import FPDF

def main():
    db=ExpenseTracker()
    if len(sys.argv)==1:
        sys.exit("Send Request [ADD|SEARCH|REPORT]")
    command=sys.argv[1].lower()
    commands={
        "add":lambda:add_expense(db),
        "search":lambda:search_expense(db),
        "report":lambda:monthly_report(db)
    }
    try:
        commands[command]()
    except KeyError:
        raise ValueError("Invalid Request")


from tabulate import tabulate


def monthly_report(db):
    month = input("Enter month name (or press Enter for all): ").strip()
    report = db.monthly_report(month) if month else db.monthly_report()

    rows = (
        [(month, report["total_spent"], report["total_receive"])]
        if month
        else [
            (item["month"], item["data"]["total_spent"], item["data"]["total_receive"])
            for item in report
            if item["data"]["total_spent"] or item["data"]["total_receive"]
        ]
    )

    if not rows:
        print("No data found.")
        return

    data=(
        tabulate(
            rows,
            headers=["Month", "Spent", "Receive"],
            tablefmt="grid",  # try: grid, pipe, pretty, rounded_grid
            floatfmt=".2f",
        )
    )
    print(data)
    choice=int(input("Do you want to save? \n1-Yes\n2-No\n"))
    if choice==1:
        to_pdf(data)
    else:
        pass

def to_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Courier",size=10)
    pdf.multi_cell(0,5,data)
    pdf.output("monthly_report.pdf")
    print("PDF saved")

def add_expense(db):
    t_types={1:"spent",2:"receive"}
    choice=int(input("TRANSACTION TYPE \n1-Spend\n2-receive\n"))

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

def search_expense(db):
    dt=input("Enter Date: ")
    dt=validate_date(dt)
    print(db.search_date(dt))


if __name__=='__main__':
    main()
