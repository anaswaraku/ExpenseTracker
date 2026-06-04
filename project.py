import sys

class ExpenseTracker:
    

def main():
    try:
        if sys.argv[1] in ['add','search','report']:
            pass
        else:
            sys.exit("Invalid command line argument")


if __name__=='__main__':
    main()