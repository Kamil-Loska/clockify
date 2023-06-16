from ReportWriter import ReportWriter


class ReportComposite(ReportWriter):

    def __init__(self, factory):
        self.factory = factory
        self.report_components = []

    def add_component(self, component):
        self.report_components.append(component)

    def remove_component(self, component):
        self.report_components.remove(component)

    def write(self, report_entries, report_writer):
        for component in self.report_components:
            if isinstance(component, report_writer):
                component.write(report_entries)
