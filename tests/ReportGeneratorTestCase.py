import unittest
from unittest.mock import MagicMock
from ReportGenerator import ReportGenerator
from ReportStrategy import ReportStrategy


class ReportGeneratorTest(unittest.TestCase):
    def setUp(self):
        self.mock_strategy = MagicMock(spec=ReportStrategy)
        self.report_generator = ReportGenerator(self.mock_strategy)
        self.test_data = [
            {"user_id": "user1", "date": "2023-06-20", "durationTime": "01:30:00"},
            {"user_id": "user2", "date": "2023-06-20", "durationTime": "00:35:15"}
        ]

    def test_strategy_property(self):
        self.assertEqual(self.report_generator._strategy, self.mock_strategy)

    def test_call_correctly_write_report_method(self):
        self.report_generator.write_report(self.test_data)
        self.mock_strategy.write_report.assert_called_once_with(self.test_data)

    def test_write_report_no_strategy(self):
        report_generator = ReportGenerator(None)
        with self.assertRaises(AttributeError):
            report_generator.write_report(self.test_data)
