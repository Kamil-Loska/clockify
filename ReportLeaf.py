from abc import ABC

from GenerateReportComposite import ReportComponent


class ReportLeaf(ReportComponent, ABC):

    def __init__(self, report_data):
        self.report_data = report_data

    def generate_report(self):
        return self.report_data
