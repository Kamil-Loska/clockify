from abc import ABC, abstractmethod


class ReportComponent(ABC):
    @abstractmethod
    def generate_report(self):
        pass
