import unittest
from unittest.mock import patch
from ConfigFileHandler import ConfigFileHandler
from CsvReportWriter import CsvReportWriter
from FieldMapper import FieldMapper


class CsvReportWriterTest(unittest.TestCase):

    def setUp(self):
        self.config_handler = ConfigFileHandler('mock_config.ini')

    @patch('builtins.open')
    @patch('csv.DictWriter.writerows')
    def test_write_report(self, mock_writerows, mock_open):
        writer = CsvReportWriter(self.config_handler)

        report_entries = [
            {'fullName': 'John Doe', 'date': '2023-05-15', 'durationTime': '1H30M',
             'taskDescription': 'Task 1'}]
        mapped_report_data = list(FieldMapper(self.config_handler).map_fields(report_entries))
        writer.write_report(report_entries)
        mock_open.assert_called_once_with('report.csv', 'w', newline='', encoding='UTF8')
        mock_writerows.assert_called_once_with(mapped_report_data)

    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    @patch('csv.DictWriter.writerows')
    def test_write_report_with_unknown_field(self, mock_writerows, mock_open):
        writer = CsvReportWriter(self.config_handler)

        report_entries = [
            {
                'fullName': 'John Doe',
                'date': '2023-05-15',
                'durationTime': '1H30M',
                'taskDescription': 'Task 1',
                'position': ''
            }
        ]

        mapped_report_data = list(FieldMapper(self.config_handler).map_fields(report_entries))
        writer.write_report(report_entries)
        mock_open.assert_called_once_with('report.csv', 'w', newline='', encoding='UTF8')
        mock_writerows.assert_called_once_with(mapped_report_data)
