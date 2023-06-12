from GenerateReportComposite import ReportComponent


class ReportComposite(ReportComponent):

    def __init__(self):
        self.report_components = []

    def add_component(self, component):
        self.report_components.append(component)

    def remove_component(self, component):
        self.report_components.remove(component)

    def generate_report(self):
        report_entries = []
        for component in self.report_components:
            report_entries.append(component.generate_report())
        return report_entries
