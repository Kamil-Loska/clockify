import csv
import os
import tempfile
import unittest
from unittest.mock import MagicMock, patch
from ClockifyReportGenerator import ClockifyReportGenerator
from ConfigFileHandler import ConfigFileHandler


class ClockifyReportGeneratorTest(unittest.TestCase):

    def setUp(self):
        self.config_handler = ConfigFileHandler('mock_config.ini')
        self.config_handler_mock = MagicMock()
        self.clockify_api_mock = MagicMock()
        self.clockify_report_generator = ClockifyReportGenerator(self.config_handler_mock, self.clockify_api_mock)

    def test_generate_csv_report(self):
        report_entries = [
            {
                'Fullname': 'John Doe',
                'Date': '2023-06-01',
                'Duration-time': '1h 30m',
                'Task-description': 'Task 1',
            },
            {
                'Fullname': 'John Doe',
                'Date': '2023-06-02',
                'Duration-time': '2h',
                'Task-description': 'Task 2',
            }
        ]

        self.clockify_report_generator.generate_csv_report(report_entries)

        filename = 'report.csv'
        self.assertTrue(os.path.exists(filename))

        file_size = os.path.getsize(filename)
        self.assertGreater(file_size, 0)

    def test_generate_xml_report(self):
        report_entries = [
            {
                'Fullname': 'John Doe',
                'Date': '2023-06-01',
                'Duration-time': '1h 30m',
                'Task-description': 'Task 1',
            },
            {
                'Fullname': 'John Doe',
                'Date': '2023-06-02',
                'Duration-time': '2h',
                'Task-description': 'Task 2',
            }
        ]

        self.clockify_report_generator.generate_xml_report(report_entries)

        filename = 'report.xml'
        self.assertTrue(os.path.exists(filename))

        file_size = os.path.getsize(filename)
        self.assertGreater(file_size, 0)

    @patch('builtins.print')
    def test_generate_console_report(self, mock_print):
        expected_report_entries = [
            {
                'Fullname': 'Doe-John',
                'Date': '2023-01-15',
                'Duration-time': '2h',
                'Task-description': 'Task 2',
            }
        ]
        self.clockify_report_generator.generate_console_report(expected_report_entries)

        self.assertEqual(mock_print.call_count, 1)

        printed_data = mock_print.call_args[0][0]
        expected_data = {'Fullname': 'Doe-John', 'Date': '2023-01-15', 'Duration-time': '2h',
                         'Task-description': 'Task 2'}
        self.assertEqual(printed_data, expected_data)

    def test_format_duration(self):
        duration = 'PT2H30M45S'
        formatted_duration = self.clockify_report_generator.format_duration(duration)
        self.assertEqual(formatted_duration, '2H 30M 45S')

        duration = 'PT1H'
        formatted_duration = self.clockify_report_generator.format_duration(duration)
        self.assertEqual(formatted_duration, '1H')

        duration = 'PT45M'
        formatted_duration = self.clockify_report_generator.format_duration(duration)
        self.assertEqual(formatted_duration, '45M')

        duration = 'PT30S'
        formatted_duration = self.clockify_report_generator.format_duration(duration)
        self.assertEqual(formatted_duration, '30S')

        duration = 'PT'
        formatted_duration = self.clockify_report_generator.format_duration(duration)
        self.assertEqual(formatted_duration, '')

    def test_empty_format_duration(self):
        duration = ''
        formatted_duration = self.clockify_report_generator.format_duration(duration)
        self.assertEqual(formatted_duration, duration)

    def test_generate_report_with_missing_time_interval(self):
        mock_config_handler = MagicMock()
        time_entries = [
            {
                'timeInterval': {'start': '2023-01-01T09:00:00Z', 'duration': 'PT1H30M'},
                'description': 'Task 1'
            },
        ]

        self.clockify_api_mock.get_time_entries_per_user.return_value = time_entries
        self.clockify_api_mock.get_user_name.return_value = 'John Doe'
        report_generator = ClockifyReportGenerator(mock_config_handler, self.clockify_api_mock)
        user_credentials = {'User_ID': '123', 'API_KEY': 'API_KEY'}
        date_from = '2023-01-01'
        date_to = '2023-01-01'
        output_format = 'console'
        result = report_generator.generate_report(user_credentials, date_from, date_to, output_format)

        self.assertEqual(result, None)
