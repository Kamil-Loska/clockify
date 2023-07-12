import sys
import unittest
from datetime import date, timedelta
from unittest.mock import patch
from Argument_provider import ArgumentProvider


class ArgumentProviderTestCase(unittest.TestCase):

    @patch('argparse.ArgumentParser.error')
    def test_argument_parser_valid_arguments(self, mock_error):
        sys.argv = ['app.py', '--from=2023-05-15', '--to=2023-05-16', '--format=csv']
        argument_provider = ArgumentProvider()
        args = argument_provider.get_arguments()
        self.assertEqual(args.date_from, '2023-05-15')
        self.assertEqual(args.date_to, '2023-05-16')
        mock_error.assert_not_called()

    @patch('argparse.ArgumentParser.error')
    def test_argument_parser_error_called(self, mock_error):
        sys.argv = ['app.py', '--from=2023-05-', '--to=2023-05-', '--format=console']
        argument_provider = ArgumentProvider()
        args = argument_provider.get_arguments()
        self.assertEqual(args.date_from, '2023-05-')
        self.assertEqual(args.date_to, '2023-05-')
        mock_error.assert_called()

    @patch('argparse.ArgumentParser.error')
    def test_format_default_value(self, mock_error):
        sys.argv = ['app.py', '--from=2023-05-15', '--to=2023-06-20']
        argument_provider = ArgumentProvider()
        args = argument_provider.get_arguments()
        self.assertEqual(args.output_format, 'console')
        mock_error.assert_not_called()

    def test_first_date_greater_than_second(self):
        first_date = '2023-06-01'
        second_date = '2023-05-15'
        with self.assertRaises(Exception):
            argument_provider = ArgumentProvider()
            argument_provider.validate_date_format(first_date, second_date)

    def test_date_validation_error_for_future_dates(self):
        today = date.today().isoformat()
        tomorrow = (date.today() + timedelta(days=1)).isoformat()
        with self.assertRaises(Exception):
            argument_provider = ArgumentProvider()
            argument_provider.validate_date_format(today, tomorrow)
