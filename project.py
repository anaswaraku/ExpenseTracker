import sys,csv
from datetime import datetime

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
    with open("expense.csv", "a") as file:
        writer=csv.DictWriter(file,fieldnames=["Date","Amount","TransactionType","Notes"])
        writer.writerow({
            "Date":expense['date'],
            "Amount":expense['amount'],
            "TransactionType": expense['t_type'],
            "Notes":expense['note']
        })



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
