from ReportStrategy import ReportStrategy
from typing import List, Dict


class ConsoleReportWriter(ReportStrategy):

    def write_report(self, report_data: List[Dict[str, str]]):
        print(','.join(report_data[0].keys()))
        for data in report_data:
            print(','.join(data.values()))
