import unittest
from unittest.mock import MagicMock
from ClockifyReportGenerator import ClockifyReportGenerator
from User import User


class ClockifyReportGeneratorTest(unittest.TestCase):

    def setUp(self):
        self.clockify_api_mock = MagicMock()
        self.clockify_report_generator = ClockifyReportGenerator(self.clockify_api_mock)
        self.mock_user = [User("1", "API_KEY", "IT Security")]

    def test_generate_report_returns_expected_output_for_given_input(self):
        self.clockify_api_mock.get_user_name.return_value = "John Doe"
        self.clockify_api_mock.get_time_entries_per_user.return_value = [
            {
                'timeInterval': {'start': '2023-05-15T00:00:00Z', 'duration': 'PT1H'},
                'description': 'Test 1',
            }
        ]
        expected_report = [
            {
                'fullName': 'John Doe',
                'department': 'IT Security',
                'date': '2023-05-15',
                'durationTime': '01:00:00',
                'taskDescription': 'Test 1',
            }
        ]

        report = self.clockify_report_generator.generate_report(self.mock_user, '2023-05-01', '2023-05-31')
        self.assertEqual(report, expected_report)

    def test_generate_report_valid_data(self):
        self.clockify_api_mock.get_user_name.return_value = "John Doe"
        self.clockify_api_mock.get_time_entries_per_user.return_value = [
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

        self.assertEqual(len(report), 2)

    def test_format_duration(self):
        duration = 'PT2H30M45S'
        formatted_duration = self.clockify_report_generator.format_duration(duration)
        self.assertEqual(formatted_duration, '02:30:45')

        duration = 'PT1H'
        formatted_duration = self.clockify_report_generator.format_duration(duration)
        self.assertEqual(formatted_duration, '01:00:00')

        duration = 'PT45M'
        formatted_duration = self.clockify_report_generator.format_duration(duration)
        self.assertEqual(formatted_duration, '00:45:00')

        duration = 'PT30S'
        formatted_duration = self.clockify_report_generator.format_duration(duration)
        self.assertEqual(formatted_duration, '00:00:30')

        duration = 'PT'
        formatted_duration = self.clockify_report_generator.format_duration(duration)
        self.assertEqual(formatted_duration, '00:00:00')

    def test_format_duration_empty_string(self):
        duration = ''
        formatted_duration = self.clockify_report_generator.format_duration(duration)
        self.assertEqual(formatted_duration, '00:00:00')

    def test_generate_report_with_missing_time_interval(self):
        self.clockify_api_mock.get_user_name.return_value = "John Doe"
        time_entries = []

        self.clockify_api_mock.get_time_entries_per_user.return_value = time_entries
        result = self.clockify_report_generator.generate_report(self.mock_user, '2023-05-01', '2023-05-31')
        self.assertEqual(result, [])
