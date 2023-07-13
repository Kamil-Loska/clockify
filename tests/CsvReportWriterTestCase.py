import unittest
from unittest.mock import patch, MagicMock

from ConfigFileHandler import ConfigFileHandler
from CsvReportWriter import CsvReportWriter
from FieldMapper import FieldMapper


class CsvReportWriterTest(unittest.TestCase):

    def setUp(self):
        self.config_handler = ConfigFileHandler('mock_config.ini')
        self.field_mapper = FieldMapper(self.config_handler)

    @patch('builtins.open')
    @patch('csv.DictWriter.writerow')
    @patch('csv.DictWriter.writerows')
    def test_write_report(self, mock_writerows, mock_writerow, mock_open):
        writer = CsvReportWriter(self.field_mapper)

        report_entries = [
            {'fullName': 'John Doe', 'date': '2023-05-15', 'durationTime': '1H30M',
             'taskDescription': 'Task 1'}]
        mapped_report_entries = [
            {'imieNazwisko': 'John Doe', 'data': '2023-05-15', 'czasTrwania': '1H30M', 'opisZadania': 'Task 1'}
        ]
        writer.write_report(report_entries)

        mock_open.assert_called_once_with('report.csv', 'w', newline='', encoding='UTF8')
        fieldnames = dict(zip(report_entries[0].keys(), mapped_report_entries[0].keys()))

        mock_writerow.assert_called_once_with(fieldnames)
        mock_writerows.assert_called_once_with(report_entries)

    @patch('builtins.open')
    def test_write_report_with_unknown_field(self, mock_open):
        writer = CsvReportWriter(self.field_mapper)

        report_entries = [
            {
                'fullName': 'John Doe',
                'date': '2023-05-15',
                'durationTime': '1H30M',
                'taskDescription': 'Task 1',
                'position': ''
            }
        ]
        mapped_report_data = list(self.field_mapper.map_fields(report_entries))
        writer.write_report(report_entries)
        mock_open.assert_called_once_with('report.csv', 'w', newline='', encoding='UTF8')
        self.assertEqual(['imieNazwisko', 'data', 'czasTrwania', 'opisZadania', 'position'],
                         list(mapped_report_data[0].keys()))
