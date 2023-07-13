import csv

from FieldMapper import FieldMapper
from ReportStrategy import ReportStrategy


class CsvReportWriter(ReportStrategy):

    def __init__(self, field_mapper: FieldMapper):
        self.field_mapper = field_mapper

    def write_report(self, report_entries: list[dict[str, str]]):
        filename = 'report.csv'
        with open(filename, 'w', newline='', encoding='UTF8') as csvfile:
            fieldnames = report_entries[0].keys()
            translated_fieldnames = next(self.field_mapper.map_fields(report_entries))
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(dict(zip(fieldnames, translated_fieldnames)))
            writer.writerows(report_entries)
            print(csvfile.name)
