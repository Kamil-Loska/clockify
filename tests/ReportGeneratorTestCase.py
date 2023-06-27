import unittest
from unittest.mock import MagicMock

from ReportGenerator import ReportGenerator


class ReportGeneratorTest(unittest.TestCase):
    def setUp(self):
        self.test_strategy = MagicMock()
        self.report_generator = ReportGenerator(self.test_strategy)
        self.report_data = [{'name': 'John Doe', 'time': '9:00'}]
        self.test_strategy.write_report.return_value = self.report_data

    def test_strategy_property(self):
        self.assertEqual(self.report_generator.strategy, self.test_strategy)

    def test_write_report(self):
        result = self.report_generator.strategy.write_report(self.report_data)
        self.assertEqual(result, self.report_data)

    def test_set_strategy(self):
        new_strategy = MagicMock()
        self.report_generator.strategy = new_strategy
        self.assertEqual(self.report_generator.strategy, new_strategy)

    def test_write_report_no_strategy(self):
        self.report_generator.strategy = None
        with self.assertRaises(AttributeError):
            self.report_generator.write_report(self.report_data)
