from __future__ import annotations
from ReportStrategy import ReportStrategy


class ReportGenerator:

    def __init__(self, strategy: ReportStrategy):
        self._strategy = strategy

    @property
    def strategy(self) -> ReportStrategy:
        return self._strategy

    def write_report(self, report_entries: list[dict[str, str]]):
        self.strategy.write_report(report_entries)
