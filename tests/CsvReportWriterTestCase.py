import unittest
from unittest.mock import patch, MagicMock
from CsvReportWriter import CsvReportWriter


class CsvReportWriterTest(unittest.TestCase):

    @patch('csv.DictWriter')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_write(self, mock_open, mock_dict_writer):
        mock_config_handler = MagicMock()
        writer = CsvReportWriter(mock_config_handler)

        report_entries = [{'fullName': 'John Doe', 'date': '2023-05-15', 'durationTime':
            '1H30M', 'taskDescription': 'Task 1'}]

        writer.write(report_entries)
        mock_open.assert_called_once_with('report.csv', 'w', newline='', encoding='UTF8')
        mock_dict_writer.assert_called_once_with(mock_open.return_value, fieldnames=[
            'fullName', 'date', 'durationTime', 'taskDescription'])
