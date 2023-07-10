from ReportStrategy import ReportStrategy
from FieldMapper import FieldMapper


class ConsoleReportWriter(ReportStrategy):

    def __init__(self, config_handler):
        self.field_mapper = FieldMapper(config_handler)

    def write_report(self, report_data: list[dict[str, str]]):
        mapped_report_data = list(self.field_mapper.map_fields(report_data))
        fieldnames = mapped_report_data[0].keys()
        print(','.join(fieldnames))
        for data in mapped_report_data:
            print(','.join(data.values()))
