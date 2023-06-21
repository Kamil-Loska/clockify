from abc import ABC, abstractmethod
from typing import List, Dict


class ReportStrategy(ABC):
    @abstractmethod
    def write_report(self, report_data: List[Dict[str, str]]):
        pass
