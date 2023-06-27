from ReportStrategy import ReportStrategy


class ConsoleReportWriter(ReportStrategy):

    def write_report(self, report_data: list[dict[str, str]]):
        print(','.join(report_data[0].keys()))
        for data in report_data:
            print(','.join(data.values()))
