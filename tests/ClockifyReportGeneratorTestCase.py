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
        self.clockify_report_generator.clockify_api = self.clockify_api_mock

        self.clockify_api_mock.get_user_name.return_value = "John Doe"
        self.clockify_api_mock.get_time_entries_per_user.return_value = [
            {
                'timeInterval': {'start': '2023-05-15T00:00:00Z', 'duration': 'PT1H'},
                'description': 'Test 1',
            },
        ]

        report = self.clockify_report_generator.generate_report(self.mock_user, '2023-05-01', '2023-05-31')

        self.assertEqual(len(report), 2)

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
        time_entries = [
            {
                'timeInterval': {'start': '2023-05-15T09:00:00Z', 'duration': 'PT1H30M'},
                'description': 'Task 1'
            },
        ]

        self.clockify_api_mock.get_time_entries_per_user.return_value = time_entries
        self.clockify_api_mock.get_user_name.return_value = 'John Doe'
        result = self.clockify_report_generator.generate_report(self.mock_user, '2023-01-01', '2023-01-01')
        self.assertEqual(result, [])
