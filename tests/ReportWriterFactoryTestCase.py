import unittest
from unittest.mock import patch, MagicMock
from ReportWriterFactory import ReportWriterFactory


class ReportWriterFactoryTest(unittest.TestCase):

    @patch('ReportWriterFactory.ConsoleReportWriter')
    def test_create_report_writer_console(self, mock_console_report_writer):
        mock_config_handler = MagicMock()
        factory = ReportWriterFactory(mock_config_handler)
        factory.create_report_writer('console')
        mock_console_report_writer.assert_called_once()

    @patch('ReportWriterFactory.CsvReportWriter')
    def test_create_report_writer_csv(self, mock_csv_report_writer):
        mock_config_handler = MagicMock()
        factory = ReportWriterFactory(mock_config_handler)
        factory.create_report_writer('csv')
        mock_csv_report_writer.assert_called_once_with(mock_config_handler)

    @patch('ReportWriterFactory.XmlReportWriter')
    def test_create_report_writer_xml(self, mock_xml_report_writer):
        mock_config_handler = MagicMock()
        factory = ReportWriterFactory(mock_config_handler)
        factory.create_report_writer('xml')
        mock_xml_report_writer.assert_called_once()

    def test_create_report_writer_invalid(self):
        mock_config_handler = MagicMock()
        factory = ReportWriterFactory(mock_config_handler)
        with self.assertRaises(TypeError):
            factory.create_report_writer('invalid')
