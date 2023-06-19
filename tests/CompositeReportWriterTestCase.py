import unittest
from unittest.mock import Mock, MagicMock
from CompositeReportWriter import ReportComposite
from ReportWriter import ReportWriter


class TestReportComposite(unittest.TestCase):
    def setUp(self):
        self.report_writer = ReportWriter
        self.composite = ReportComposite(self.report_writer)
        self.mock_report_writer = MagicMock(spec=self.report_writer)

    def test_add_component(self):
        component = Mock()
        self.composite.add_component(component)
        self.assertIn(component, self.composite.report_components)

    def test_remove_component(self):
        component = Mock()
        self.composite.add_component(component)
        self.assertIn(component, self.composite.report_components)

        self.composite.remove_component(component)
        self.assertNotIn(component, self.composite.report_components)

    def test_write(self):
        self.mock_report_writer.write = MagicMock()
        self.composite.add_component(self.mock_report_writer)

        entries = [{'entry 1'}, {'entry 2'}]
        self.composite.write(entries)

        self.mock_report_writer.write.assert_called_once_with(entries)