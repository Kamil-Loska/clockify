from ConsoleReportWriter import ConsoleReportWriter
from XmlReportWriter import XmlReportWriter
from CsvReportWriter import CsvReportWriter


class ReportWriterFactory:

    def __init__(self, config_handler):
        self.output_format = {
            'console': self.create_console_report_writer,
            'csv': self.create_csv_report_writer,
            'xml': self.create_xml_report_writer
        }
        self.config_handler = config_handler

    def create_console_report_writer(self):
        return ConsoleReportWriter()

    def create_csv_report_writer(self):
        return CsvReportWriter(self.config_handler)

    def create_xml_report_writer(self):
        return XmlReportWriter()

    def create_report_writer(self, output_format):
        report_writer_method = self.output_format.get(output_format)

        return report_writer_method()
