from main import ClockifyApp
from parser import parse_arguments

def main():
    args = parse_arguments()
    clockify = ClockifyApp()
    clockify.generate_raport(args.date_from, args.date_to)

if __name__ == '__main__':
    main()