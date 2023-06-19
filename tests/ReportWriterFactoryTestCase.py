import unittest
from ConsoleReportWriter import ConsoleReportWriter
from CsvReportWriter import CsvReportWriter
from ReportWriterFactory import ReportWriterFactory
from XmlReportWriter import XmlReportWriter


class TestReportWriterFactory(unittest.TestCase):
    def setUp(self):
        self.factory = ReportWriterFactory()

    def test_get_report_writer_type_console(self):
        writer = self.factory.get_report_writer_type('console')
        self.assertEqual(writer, ConsoleReportWriter)

    def test_get_report_writer_type_csv(self):
        writer = self.factory.get_report_writer_type('csv')
        self.assertEqual(writer, CsvReportWriter)

    def test_get_report_writer_type_xml(self):
        writer = self.factory.get_report_writer_type('xml')
        self.assertEqual(writer, XmlReportWriter)

    def test_get_report_writer_type_invalid(self):
        with self.assertRaises(KeyError):
            self.factory.get_report_writer_type('invalid')
