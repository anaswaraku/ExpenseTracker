import sys

def main():

    if len(sys.argv)==1:
        sys.exit("Send Request")
    elif sys.argv[1] in ['add','search','update']:
            pass
    else:
        raise ValueError("Invalid Request")

    t_types={1:"send",2:"recieve"}
    request_map={
        "add": add_expense}


def add_expense():

    expense={
        "date":input("DATE: "),
        "amount":float(input("AMOUNT: ")),
        "t_type":t_types[input("TRANSACTION TYPE \n1-Send\2-Recieve")]
        "note"":"input("NOTE: ")
    }
    prin(expense)


def search_expense():
    pass


def update_expense():
    pass


if __name__=='__main__':
    main()
