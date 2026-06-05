import sys

class ExpenseTracker:

    def __init__(self,date,amount,transaction_type,purpose):
        self.date = date
        self.amount = amount
        self.transaction_type = transaction_type
        self.purpose = purpose

        if self.type not in ['spend','recieve']:
            raise ValueError("Type can be either Spend/Receive")
def main():

    if len(sys.argv)==1:
        sys.exit("Send Request")
    elif sys.argv[1] in ['add','search','update']:
            pass
    else:
        raise ValueError("Invalid Request")

    request_map={
        "add": add_expense}

def add_expense():
    expense = ExpenseTracker(
        date=input(),
        amount=input(),
        transaction_type=input(),
        purpose=input(),
    )
    return expense


def search_expense():
    pass


def update_expense():
    pass


if __name__=='__main__':
    main()
