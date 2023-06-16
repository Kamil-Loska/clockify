from ConsoleReportWriter import ConsoleReportWriter
from XmlReportWriter import XmlReportWriter
from CsvReportWriter import CsvReportWriter


class ReportWriterFactory:

    def get_report_writer_type(self, output_format):
        format_output = {
            'console': ConsoleReportWriter,
            'csv': CsvReportWriter,
            'xml': XmlReportWriter
        }
        return format_output[output_format]
