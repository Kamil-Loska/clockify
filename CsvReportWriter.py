import csv
from ReportStrategy import ReportStrategy
from ConfigFileHandler import ConfigFileHandler


class CsvReportWriter(ReportStrategy):

    def __init__(self, config_handler: ConfigFileHandler):
        self.config_handler = config_handler

    def write_report(self, report_entries: list[dict[str, str]]):
        filename = 'report.csv'
        with open(filename, 'w', newline='', encoding='UTF8') as csvfile:
            fieldnames = list(report_entries[0].keys())
            translated_fieldnames = [self.config_handler.translation_mapper().get(fieldname, fieldname)
                                     for fieldname in fieldnames]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(dict(zip(fieldnames, translated_fieldnames)))
            writer.writerows(report_entries)

            print(csvfile.name)
