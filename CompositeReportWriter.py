from ReportWriter import ReportWriter


class ReportComposite(ReportWriter):

    def __init__(self):
        self.report_components = []

    def add_component(self, component):
        self.report_components.append(component)

    def remove_component(self, component):
        self.report_components.remove(component)

    def write(self, report_entries):
        for component in self.report_components:
            component.write(report_entries)
