import unittest
from unittest.mock import MagicMock
from ClockifyReportGenerator import ClockifyReportGenerator


class ClockifyReportGeneratorTest(unittest.TestCase):

    def setUp(self):
        self.config_handler_mock = MagicMock()
        self.clockify_api_mock = MagicMock()
        self.clockify_report_generator = ClockifyReportGenerator(self.config_handler_mock, self.clockify_api_mock)

    def test_generate_report_returns_expected_report_entries(self):
        time_entries = [
            {
                'timeInterval': {
                    'start': '2023-01-15T00:00:00Z',
                    'end': '2023-01-15T23:59:59Z',
                    'duration': 'PT2H'
                },
                'description': 'Task 1'
            }
        ]
        user_name = 'John Doe'
        self.clockify_api_mock.get_time_entries_per_user.return_value = time_entries
        self.clockify_api_mock.get_user_name.return_value = user_name
        self.config_handler_mock.translation_mapper.return_value = {
            'Fullname': 'Full Name',
            'Date': 'Date',
            'Duration-time': 'Duration',
            'Task-description': 'Description'
        }

        expected_report_entries = [
            {
                'Full Name': 'Doe-John',
                'Date': '2023-01-15',
                'Duration': '2H',
                'Description': 'Task 1'
            }
        ]

        report = self.clockify_report_generator.generate_report('user_token', '2023-05-15', '2023-06-02')
        self.assertEqual(report, expected_report_entries)


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