import sys
from main import ClockifyApp

def main():
    clockify = ClockifyApp()
    if len(sys.argv) != 3:
        print("Invalid number of arguments. Please provide two dates as arguments")
        return
    date_from = sys.argv[1]
    date_to = sys.argv[2]
    if not clockify.validate_date_format(date_from, date_to):
        print("Invalid date format. Please provide dates in the format 'YYYY-MM-DD'. ")
        return
    clockify.generate_raport(date_from, date_to)

if __name__ == '__main__':
    main()