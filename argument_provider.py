import argparse
from datetime import datetime


class ArgumentProvider:

    def validate_date_format(self, date_from, date_to):
        try:
            datetime.strptime(date_from, '%Y-%m-%d')
            datetime.strptime(date_to, '%Y-%m-%d')
            if date_from > date_to:
                print("First date can't be greater than second date")
                return False
            return True
        except ValueError:
            return False

    def get_arguments(self):
        parser = argparse.ArgumentParser(description='Generate Clockify report')
        parser.add_argument('--from', dest='date_from', required=True, help='Start date (YYYY-MM-DD)')
        parser.add_argument('--to', dest='date_to', required=True, help='End date (YYYY-MM-DD)')
        parser.add_argument('--format', dest='output_format', required=False, help='Output format (CSV | XML | Console)',
                            default='console', choices=['csv', 'xml', 'console'])
        args = parser.parse_args()
        if not self.validate_date_format(args.date_from, args.date_to):
            parser.error("Invalid date format! Please provide dates in YYYY-MM-DD format.")

        return args
