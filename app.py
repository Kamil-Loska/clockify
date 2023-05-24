import sys
from main import ClockifyApp

if __name__ == '__main__':
    clockify = ClockifyApp()
    date_from = sys.argv[1]
    date_to = sys.argv[2]
    if len(sys.argv) != 3:
        print("Invalid number of arguments. Please provide two dates as arguments")
    if not clockify.validate_date_format(date_from, date_to):
        print("Invalid date format. Please provide dates in the format 'YYYY-MM-DD'. ")
    else:
        clockify.generate_raport(date_from, date_to)