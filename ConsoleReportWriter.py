from ReportStrategy import ReportStrategy


class ConsoleReportWriter(ReportStrategy):

    def __init__(self, config_handler):
        self.config_handler = config_handler
        self.translation_map = self.config_handler.translation_mapper()

    def write_report(self, report_data: list[dict[str, str]]):
        fieldnames = list(report_data[0].keys())
        translated_fieldnames = [self.translation_map.get(fieldname, fieldname)
                                 for fieldname in fieldnames]
        print(','.join(translated_fieldnames))
        for data in report_data:
            print(','.join(data.values()))
