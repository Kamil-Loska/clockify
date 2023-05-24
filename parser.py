import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Generate Clockify report')
    parser.add_argument('--from', dest='date_from', required=True, help='Start date (YYYY-MM-DD)')
    parser.add_argument('--to', dest='date_to', required=True, help='End date (YYYY-MM-DD)')
    return parser.parse_args()