import argparse
import unittest
from unittest.mock import patch
from argument_provider import ArgumentProvider


class ArgumentProviderTestCase(unittest.TestCase):

    @patch('argparse.ArgumentParser.error')
    def test_argument_parser_valid_arguments(self, mock_error):
        with patch('argparse.ArgumentParser.parse_args',
                   return_value=argparse.Namespace(date_from='2023-05-15', date_to='2023-05-16', format='csv')):
            args = ArgumentProvider().get_arguments()
        self.assertEqual(args.date_from, '2023-05-15')
        self.assertEqual(args.date_to, '2023-05-16')
        mock_error.assert_not_called()


    @patch('argparse.ArgumentParser.error')
    def test_argument_parser_error_called(self, mock_error):
        with patch('argparse.ArgumentParser.parse_args',
                   return_value=argparse.Namespace(date_from='2023-05-', date_to='2023-05-', format='console')):
                args = ArgumentProvider().get_arguments()
        self.assertEqual(args.date_from, '2023-05-')
        self.assertEqual(args.date_to, '2023-05-')
        mock_error.assert_called()
