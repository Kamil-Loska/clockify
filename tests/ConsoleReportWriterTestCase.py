import unittest
from unittest.mock import call, patch
from ConfigFileHandler import ConfigFileHandler
from ConsoleReportWriter import ConsoleReportWriter
from FieldMapper import FieldMapper


class TestConsoleReportWriter(unittest.TestCase):
    def setUp(self):
        self.config_handler = ConfigFileHandler('mock_config.ini')
        self.field_mapper = FieldMapper(self.config_handler)
        self.writer = ConsoleReportWriter(self.field_mapper)

    @patch('builtins.print')
    def test_write_report(self, mock_print):
        report_data = [
            {
                'fullName': 'Mock Name 1',
                'date': '2023-05-15',
                'durationTime': '01:00:00',
                'taskDescription': 'Mock Task 1'
            },
            {
                'fullName': 'Mock Name 2',
                'date': '2023-05-15',
                'durationTime': '02:45:15',
                'taskDescription': 'Mock Task 2'
            }
        ]

        self.writer.write_report(report_data)

        expected_calls = [
            call('imieNazwisko,data,czasTrwania,opisZadania'),
            call('Mock Name 1,2023-05-15,01:00:00,Mock Task 1'),
            call('Mock Name 2,2023-05-15,02:45:15,Mock Task 2')
        ]
        mock_print.assert_has_calls(expected_calls)
