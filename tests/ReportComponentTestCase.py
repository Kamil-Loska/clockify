import unittest
from unittest.mock import MagicMock
from ReportWriter import ReportWriter
from CompositeReportWriter import ReportComposite


class ReportCompositeTestCase(unittest.TestCase):

    def setUp(self):
        self.composite = ReportComposite()
        self.mock_component1 = MagicMock(spec=ReportWriter)
        self.mock_component2 = MagicMock(spec=ReportWriter)
        self.report_entries = [{'data': 'Report 1'}, {'data': 'Report 2'}]


    def test_add_component(self):
        self.composite.add_component(self.mock_component1)

        self.assertIn(self.mock_component1, self.composite.report_components)

    def test_remove_component(self):
        self.composite.add_component(self.mock_component1)
        self.composite.remove_component(self.mock_component1)

        self.assertNotIn(self.mock_component1, self.composite.report_components)

    def test_write(self):
        self.composite.add_component(self.mock_component1)
        self.composite.add_component(self.mock_component2)
        self.composite.write(self.report_entries)

        self.mock_component1.write.assert_called_once_with(self.report_entries)
        self.mock_component2.write.assert_called_once_with(self.report_entries)