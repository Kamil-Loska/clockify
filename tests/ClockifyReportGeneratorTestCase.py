import unittest
from unittest.mock import MagicMock
from ClockifyReportGenerator import ClockifyReportGenerator
import os


class TestClockifyReportGenerator(unittest.TestCase):

    def setUp(self):
        config_handler = MagicMock()
        credentials_file = MagicMock()
        self.clockify_report_generator = ClockifyReportGenerator(config_handler, credentials_file)

    def test_generate_report(self):
        os.chdir('..')
        expected_keys = ['Fullname', 'Date', 'Duration time', 'Task description']

        argument_provider = MagicMock()
        argument_provider.validate_date_format.return_value = None
        self.clockify_report_generator.argument_provider = argument_provider

        file_handler = MagicMock()
        file_handler.config = {
            'Clockify': {
                'WORKSPACE_ID': 'workspace_id'
            }
        }
        file_handler.get_users_from_file.return_value = {
            'user1': 'api_key1',
            'user2': 'api_key2'
        }
        self.clockify_report_generator.file_handler = file_handler

        clockify_api = MagicMock()
        clockify_api.get_time_entries_per_user.return_value = [
            {
                'userId': 'user1',
                'timeInterval': {'start': '2023-01-02T08:00:00Z', 'duration': 'PT2H'},
                'description': 'Task 1'
            },
            {
                'userId': 'user2',
                'timeInterval': {'start': '2023-01-03T09:00:00Z', 'duration': 'PT1H'},
                'description': ''
            },
            {
                'userId': 'user3',
                'timeInterval': {'start': '2023-01-05T10:00:00Z', 'duration': 'PT3H'},
                'description': 'Task 3'
            }
        ]
        clockify_api.get_user_name.return_value = 'John Doe'
        self.clockify_report_generator.ClockifyAPI = MagicMock(return_value=clockify_api)

        self.clockify_report_generator.generate_report('2023-01-01', '2023-01-31')

        for report_date in file_handler.translation_mapper.call_args_list:
            for key in expected_keys:
                self.assertIn(key, report_date)

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
