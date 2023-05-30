import argparse
from datetime import datetime


class ArgumentProvider:
    def validate_date_format(self, date_from, date_to):
        try:
            datetime.strptime(date_from, '%Y-%m-%d')
            datetime.strptime(date_to, '%Y-%m-%d')
            return True
        except ValueError:
            raise argparse.ArgumentTypeError(ValueError)

    def argument_parser(self):
        parser = argparse.ArgumentParser(description='Generate Clockify report')
        parser.add_argument('--from', dest='date_from', required=True, help='Start date (YYYY-MM-DD)')
        parser.add_argument('--to', dest='date_to', required=True, help='End date (YYYY-MM-DD)')
        args = parser.parse_args()

        if not self.validate_date_format(args.date_from, args.date_to):
            parser.error("Invalid date format! Please provide dates in YYYY-MM-DD format.")

        return args
