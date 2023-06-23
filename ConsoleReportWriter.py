from ReportStrategy import ReportStrategy
from typing import List, Dict


class ConsoleReportWriter(ReportStrategy):

    def write_report(self, report_data: List[Dict[str, str]]):
        for date_report in report_data:
            print(date_report)
