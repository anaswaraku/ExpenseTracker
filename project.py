import sys, csv
from datetime import datetime, date
import sqlite3
from expense import ExpenseTracker
from fpdf import FPDF


def main():
    db = ExpenseTracker()
    if len(sys.argv) == 1:
        sys.exit("Send Request [ADD|SEARCH|REPORT]")
    command = sys.argv[1].lower()
    commands = {
        "add": lambda: add_expense(db),
        "search": lambda: search_expense(db),
        "report": lambda: monthly_report(db),
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

    data = tabulate(
        rows,
        headers=["Month", "Spent", "Receive"],
        tablefmt="grid",  # try: grid, pipe, pretty, rounded_grid
        floatfmt=".2f",
    )
    print(data)
    while True:
        try:
            choice = int(input("Do you want to save? \n1-Yes\n2-No\n"))
            if choice == 1:
                to_pdf(data)
            break
        except ValueError:
            print("Invalid input. Please enter 1 or 2.")


def to_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Courier", size=10)
    pdf.multi_cell(0, 5, data)
    pdf.output("monthly_report.pdf")
    print("PDF saved")


def add_expense(db):
    t_types = {1: "spent", 2: "receive"}
    while True:
        try:
            choice = int(input("TRANSACTION TYPE \n1-Spend\n2-receive\n"))
            if choice in t_types:
                break
            else:
                print("Invalid choice. Please enter 1 or 2.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    date_str = None
    while not date_str:
        date_str = validate_date(input("DATE (e.g., 24/07/2024 or July 24, 2024): "))
        if not date_str:
            print("Invalid date format. Please try again.")

    while True:
        try:
            amount = float(input("AMOUNT: "))
            break
        except ValueError:
            print("Invalid amount. Please enter a number.")

    expense = {
        "date": date_str,
        "amount": amount,
        "t_type": t_types[choice],
        "note": input("NOTE: "),
    }
    db.add_expense(expense)


def validate_date(inp_date):
    try:
        if "/" in inp_date:
            dt = datetime.strptime(inp_date, "%d/%m/%Y")
        else:
            dt = datetime.strptime(inp_date, "%B %d, %Y")
        return dt.date().isoformat()
    except ValueError:
        return None


def search_expense(db):
    date_str = input("Enter Date (e.g., 24/07/2024 or July 24, 2024): ")
    dt = validate_date(date_str)
    if not dt:
        print("Invalid date format.")
        return

    opening_balance = db.get_balance_up_to_date(dt)
    results = db.search_date(dt)

    # Display individual transactions if any
    if results:
        headers = results[0].keys()
        rows = [list(row) for row in results]
        print(f"\nTransactions for {dt}:")
        print(tabulate(rows, headers=headers, tablefmt="grid"))
    else:
        print(f"No expenses found for date: {dt}")

    # Calculate and display totals
    total_spent = sum(
        float(r["amount"]) for r in results if r["transaction_type"] == "spent"
    )
    total_received = sum(
        float(r["amount"]) for r in results if r["transaction_type"] == "receive"
    )
    net_change = total_received - total_spent
    closing_balance = opening_balance + net_change

    print("\n--- Summary for the day ---")
    print(f"Opening Balance: {opening_balance:.2f}")
    print(f"Total Spent: {total_spent:.2f}")
    print(f"Total Received: {total_received:.2f}")
    print(f"Net Change: {net_change:.2f}")
    print(f"Closing Balance: {closing_balance:.2f}")


if __name__ == "__main__":
    main()
