import csv
from ReportWriter import ReportWriter


class CsvReportWriter(ReportWriter):

    def __init__(self, config_handler):
        self.config_handler = config_handler

    def write(self, report_entries):
        filename = 'report.csv'
        with open(filename, 'w', newline='', encoding='UTF8') as csvfile:
            fieldnames = list(report_entries[0].keys())
            translated_fieldnames = [self.config_handler.translation_mapper().get(fieldname, fieldname)
                                     for fieldname in fieldnames]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(dict(zip(fieldnames, translated_fieldnames)))

            for report_data in report_entries:
                writer.writerow(report_data)

        print(csvfile.name)
