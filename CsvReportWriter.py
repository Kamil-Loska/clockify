import csv
from ReportStrategy import ReportStrategy
from ConfigFileHandler import ConfigFileHandler
from FieldMapper import FieldMapper


class CsvReportWriter(ReportStrategy):

    def __init__(self, config_handler: ConfigFileHandler):
        self.field_mapper = FieldMapper(config_handler)

    def write_report(self, report_entries: list[dict[str, str]]):
        filename = 'report.csv'
        with open(filename, 'w', newline='', encoding='UTF8') as csvfile:
            mapped_report_data = list(self.field_mapper.map_fields(report_entries))
            fieldnames = mapped_report_data[0].keys()

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(mapped_report_data)

            print(csvfile.name)
