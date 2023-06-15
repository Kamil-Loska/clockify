import unittest
from unittest.mock import MagicMock
from ClockifyReportGenerator import ClockifyReportGenerator
from ConfigFileHandler import ConfigFileHandler


class ClockifyReportGeneratorTest(unittest.TestCase):

    def setUp(self):
        self.config_handler = ConfigFileHandler('mock_config.ini')
        self.config_handler_mock = MagicMock()
        self.clockify_api_mock = MagicMock()
        self.clockify_report_generator = ClockifyReportGenerator(self.config_handler_mock, self.clockify_api_mock)
        self.mock_user = {"API_KEY": "test_key", "User_ID": "test_user_id"}

    def test_generate_report_valid_data(self):
        mock_clockify_api = MagicMock()
        self.clockify_report_generator.clockify_api = mock_clockify_api

        mock_clockify_api.get_user_name.return_value = "John Doe"
        mock_clockify_api.get_time_entries_per_user.return_value = [
            {
                'timeInterval': {'start': '2023-05-15T00:00:00Z', 'duration': 'PT1H'},
                'description': 'Test 1',
            },
            {
                'timeInterval': {'start': '2023-05-15T00:00:00Z', 'duration': 'PT2H'},
                'description': '',
            },
        ]

        report = self.clockify_report_generator.generate_report(self.mock_user, '2023-05-01', '2023-05-31')

        self.assertEqual(len(report), 4)

    def test_format_duration(self):
        duration = 'PT2H30M45S'
        formatted_duration = self.clockify_report_generator.format_duration(duration)
        self.assertEqual(formatted_duration, '2H30M45S')

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
                'timeInterval': {'start': '2023-05-15T09:00:00Z', 'duration': 'PT1H30M'},
                'description': 'Task 1'
            },
        ]

        self.clockify_api_mock.get_time_entries_per_user.return_value = time_entries
        self.clockify_api_mock.get_user_name.return_value = 'John Doe'
        report_generator = ClockifyReportGenerator(mock_config_handler, self.clockify_api_mock)
        user_credentials = [{'User_ID': '123', 'API_KEY': 'API_KEY'}]
        date_from = '2023-01-01'
        date_to = '2023-01-01'
        result = report_generator.generate_report(user_credentials, date_from, date_to)
        self.assertEqual(result, [])
