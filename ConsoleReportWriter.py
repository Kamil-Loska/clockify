from ReportStrategy import ReportStrategy


class ConsoleReportWriter(ReportStrategy):

    def __init__(self, field_mapper):
        self.field_mapper = field_mapper

    def write_report(self, report_data: list[dict[str, str]]):
        fieldnames = next(self.field_mapper.map_fields(report_data))
        print(','.join(fieldnames))
        for data in report_data:
            print(','.join(data.values()))
