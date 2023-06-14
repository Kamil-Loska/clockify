from abc import ABC, abstractmethod


class ReportWriter(ABC):
    @abstractmethod
    def write(self, report_entries):
        pass
