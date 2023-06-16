import unittest
from unittest.mock import patch, MagicMock
from ReportWriterFactory import ReportWriterFactory
from ConsoleReportWriter import ConsoleReportWriter
from CsvReportWriter import CsvReportWriter
from XmlReportWriter import XmlReportWriter


class ReportWriterFactoryTest(unittest.TestCase):

    @patch.object(ConsoleReportWriter, '__init__', return_value=None)
    def test_create_report_writer_console(self, mock_console_report_writer):
        mock_config_handler = MagicMock()
        factory = ReportWriterFactory(mock_config_handler)
        factory.create_report_writer(ConsoleReportWriter)
        mock_console_report_writer.assert_called_once()

    @patch.object(CsvReportWriter, '__init__', return_value=None)
    def test_create_report_writer_csv(self, mock_csv_report_writer):
        mock_config_handler = MagicMock()
        factory = ReportWriterFactory(mock_config_handler)
        factory.create_report_writer(CsvReportWriter)
        mock_csv_report_writer.assert_called_once_with(mock_config_handler)

    @patch.object(XmlReportWriter, '__init__', return_value=None)
    def test_create_report_writer_xml(self, mock_xml_report_writer):
        mock_config_handler = MagicMock()
        factory = ReportWriterFactory(mock_config_handler)
        factory.create_report_writer(XmlReportWriter)
        mock_xml_report_writer.assert_called_once()

    def test_create_report_writer_invalid(self):
        mock_config_handler = MagicMock()
        factory = ReportWriterFactory(mock_config_handler)
        result = factory.create_report_writer(None)
        self.assertIsNone(result)
