from ConsoleReportWriter import ConsoleReportWriter
from XmlReportWriter import XmlReportWriter
from CsvReportWriter import CsvReportWriter


class ReportStrategyFactory:

    def __init__(self, config_handler):
        self.config_handler = config_handler

    def get_strategy(self, output_format: str) -> type:
        strategies = {
            'console': ConsoleReportWriter(),
            'csv': CsvReportWriter(self.config_handler),
            'xml': XmlReportWriter()
        }
        return strategies[output_format]
