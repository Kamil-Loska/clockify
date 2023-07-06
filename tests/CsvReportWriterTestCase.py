import unittest
from unittest.mock import patch, MagicMock
from CsvReportWriter import CsvReportWriter


class CsvReportWriterTest(unittest.TestCase):

    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    @patch('csv.DictWriter.writerow')
    @patch('csv.DictWriter.writerows')
    def test_write_report(self, mock_writerows, mock_writerow, mock_open):
        mock_config_handler = MagicMock()
        mock_config_handler.translation_mapper.return_value = {'fullName': 'FullName', 'department': 'Department',
                                                               'date': 'Date', 'durationTime':
                                                                   'Duration', 'taskDescription': 'Task Description'}

        writer = CsvReportWriter(mock_config_handler)

        report_entries = [
            {'fullName': 'John Doe', 'department': 'IT Security', 'date': '2023-05-15', 'durationTime': '1H30M',
             'taskDescription': 'Task 1'}]
        writer.write_report(report_entries)
        mock_open.assert_called_once_with('report.csv', 'w', newline='', encoding='UTF8')

        fieldnames = dict(zip(['fullName', 'department', 'date', 'durationTime', 'taskDescription'],
                              ['FullName', 'Department', 'Date', 'Duration', 'Task Description']))
        mock_writerow.assert_called_once_with(fieldnames)
        mock_writerows.assert_called_once_with(report_entries)
