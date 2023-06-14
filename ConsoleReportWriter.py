from ReportWriter import ReportWriter


class ConsoleReportWriter(ReportWriter):
    def write(self, report_entries):
        for report_data in report_entries:
            print(report_data)
