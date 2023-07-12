from ConsoleReportWriter import ConsoleReportWriter
from XmlReportWriter import XmlReportWriter
from CsvReportWriter import CsvReportWriter


class ReportStrategyFactory:

    def __init__(self, config_handler, field_mapper):
        self.config_handler = config_handler
        self.field_mapper = field_mapper

    def get_strategy(self, output_format: str):
        match output_format:
            case 'console': return ConsoleReportWriter(self.field_mapper)
            case 'csv': return CsvReportWriter(self.field_mapper)
            case 'xml': return XmlReportWriter()
            case _: raise ValueError(f"Unknown strategy: {output_format}")
