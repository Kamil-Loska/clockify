import unittest
from unittest.mock import patch
from ConsoleReportWriter import ConsoleReportWriter


class ConsoleReportWriterTest(unittest.TestCase):

    @patch('builtins.print')
    def test_write_report(self, mock_print):
        writer = ConsoleReportWriter()
        report_data = [
            {'fullName': 'Mock Name 1', 'date': '2023-01-01', 'durationTime': '1H', 'taskDescription': 'Mock Task 1'},
            {'fullName': 'Mock Name 2', 'date': '2023-01-02', 'durationTime': '2H', 'taskDescription': 'Mock Task 2'},
        ]
        writer.write_report(report_data)

        expected_calls = [
            unittest.mock.call('fullName,date,durationTime,taskDescription'),
            unittest.mock.call('Mock Name 1,2023-01-01,1H,Mock Task 1'),
            unittest.mock.call('Mock Name 2,2023-01-02,2H,Mock Task 2'),
        ]
        mock_print.assert_has_calls(expected_calls)
