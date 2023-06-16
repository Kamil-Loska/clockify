import unittest
from unittest.mock import MagicMock, Mock
from ReportWriter import ReportWriter
from CompositeReportWriter import ReportComposite
from ReportWriterFactory import ReportWriterFactory


class ReportCompositeTestCase(unittest.TestCase):

    def setUp(self):
        self.mock_factory = MagicMock(spec=ReportWriterFactory)
        self.composite = ReportComposite(self.mock_factory)
        self.mock_component1 = MagicMock(spec=ReportWriter)
        self.mock_component2 = MagicMock(spec=ReportWriter)
        self.report_entries = [{'data': 'Report 1'}, {'data': 'Report 2'}]

    def test_add_component(self):
        self.composite.add_component('mock_component1')
        self.mock_factory.create_report_writer.assert_called_once_with('mock_component1')
        self.assertIn('mock_component1', self.composite.report_components)

    def test_remove_component(self):
        self.composite.add_component('mock_component1')
        self.composite.remove_component('mock_component1')
        self.assertNotIn('mock_component1', self.composite.report_components)

    def test_write(self):
        component1 = Mock(spec=ReportWriter)
        component2 = Mock(spec=ReportWriter)
        output_format = 'console'

        self.mock_factory.get_report_writer_type.return_value = type(component1)

        self.composite.add_component(component1)
        self.composite.add_component(component2)

        self.composite.write(self.report_entries, output_format)

        component1.write.assert_called_once_with(self.report_entries)
        component2.write.assert_not_called()

