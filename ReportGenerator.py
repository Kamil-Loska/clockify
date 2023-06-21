from __future__ import annotations
from ReportStrategy import ReportStrategy
from typing import List, Dict

class ReportGenerator:

    def __init__(self, strategy: ReportStrategy = None):
        self._strategy = strategy

    @property
    def strategy(self) -> ReportStrategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: ReportStrategy):
        self._strategy = strategy

    def write_report(self, report_entries: List[Dict[str, str]]):
        self.strategy.write_report(report_entries)


