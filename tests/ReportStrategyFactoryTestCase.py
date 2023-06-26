import unittest
from unittest.mock import MagicMock
from ConsoleReportWriter import ConsoleReportWriter
from CsvReportWriter import CsvReportWriter
from ReportStrategyFactory import ReportStrategyFactory
from XmlReportWriter import XmlReportWriter


class TestReportWriterFactory(unittest.TestCase):
    def setUp(self):
        self.config_handler = MagicMock()
        self.factory = ReportStrategyFactory(self.config_handler)

    def test_get_report_writer_type_console(self):
        writer = self.factory.get_strategy('console')
        self.assertIsInstance(writer, ConsoleReportWriter)

    def test_get_report_writer_type_csv(self):
        writer = self.factory.get_strategy('csv')
        self.assertIsInstance(writer, CsvReportWriter)

    def test_get_report_writer_type_xml(self):
        writer = self.factory.get_strategy('xml')
        self.assertIsInstance(writer, XmlReportWriter)

    def test_get_report_writer_type_invalid(self):
        writer = self.factory.get_strategy('invalid')
        self.assertIsNone(writer)
