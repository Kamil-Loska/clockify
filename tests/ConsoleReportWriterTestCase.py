import unittest
from unittest.mock import patch
from ConsoleReportWriter import ConsoleReportWriter


class ConsoleReportWriterTest(unittest.TestCase):

    def setUp(self):
        self.console_report_writer = ConsoleReportWriter()

    @patch('builtins.print')
    def test_write(self, mock_print):
        report_entries = [{'fullName': 'John Doe', 'date': '2023-05-15', 'durationTime': '1H30M',
                           'taskDescription': 'Task 1'}]
        self.console_report_writer.write_report(report_entries)
        mock_print.assert_called_with(report_entries[0])
