import unittest
from unittest.mock import patch, MagicMock
from CsvReportWriter import CsvReportWriter


class CsvReportWriterTest(unittest.TestCase):

    @patch('csv.DictWriter')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_write(self, mock_open, mock_dict_writer):
        mock_config_handler = MagicMock()
        mock_config_handler.translation_mapper.return_value = {'fullName': 'Full Name', 'date': 'Date', 'durationTime':
            'Duration', 'taskDescription': 'Task Description'}

        writer = CsvReportWriter(mock_config_handler)

        mock_dict_writer_instance = mock_dict_writer.return_value
        mock_dict_writer_instance.writeheader.return_value = None
        mock_dict_writer_instance.writerow.return_value = None

        report_entries = [
            {'fullName': 'John Doe', 'date': '2023-05-15', 'durationTime': '1H30M', 'taskDescription': 'Task 1'}]

        writer.write(report_entries)

        mock_open.assert_called_once_with('report.csv', 'w', newline='', encoding='UTF8')
        mock_dict_writer.assert_called_once_with(mock_open.return_value,
                                                 fieldnames=['Full Name', 'Date', 'Duration', 'Task Description'])
        mock_dict_writer_instance.writeheader.assert_called_once()
        mock_dict_writer_instance.writerow.assert_called_once_with(
            {'Full Name': 'John Doe', 'Date': '2023-05-15', 'Duration': '1H30M', 'Task Description': 'Task 1'})
