import unittest
from unittest import mock
from unittest.mock import patch, MagicMock
from ConsoleReportWriter import ConsoleReportWriter


class ConsoleReportWriterTest(unittest.TestCase):

    @patch('builtins.print')
    def test_write_report(self, mock_print):
        mock_config_handler = MagicMock()
        mock_config_handler.translation_mapper.return_value = {'fullName': 'FullName', 'date': 'Date', 'durationTime':
            'Duration', 'taskDescription': 'Task Description'}
        writer = ConsoleReportWriter(mock_config_handler)

        report_data = [
            {'fullName': 'Mock Name 1', 'date': '2023-05-15', 'durationTime': '01:00:00', 'taskDescription':
                'Mock Task 1'},
            {'fullName': 'Mock Name 2', 'date': '2023-05-15', 'durationTime': '02:45:15', 'taskDescription':
                'Mock Task 2'},
        ]
        writer.write_report(report_data)

        expected_calls = [
            mock.call('Mock Name 1,2023-05-15,01:00:00,Mock Task 1'),
            mock.call('Mock Name 2,2023-05-15,02:45:15,Mock Task 2'),
        ]
        mock_print.assert_has_calls(expected_calls)
