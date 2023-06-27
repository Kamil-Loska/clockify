
from ConsoleReportWriter import ConsoleReportWriter
from XmlReportWriter import XmlReportWriter
from CsvReportWriter import CsvReportWriter


class ReportStrategyFactory:

    def __init__(self, config_handler):
        self.config_handler = config_handler

    def get_strategy(self, output_format: str):
        match output_format:
            case 'console': return ConsoleReportWriter()
            case 'csv': return CsvReportWriter(self.config_handler)
            case 'xml': return XmlReportWriter()
