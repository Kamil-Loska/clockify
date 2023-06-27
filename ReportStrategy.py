from abc import ABC, abstractmethod


class ReportStrategy(ABC):
    @abstractmethod
    def write_report(self, report_data: list[dict[str, str]]):
        pass
