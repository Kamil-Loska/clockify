import unittest
from unittest.mock import MagicMock

from GenerateReportComposite import ReportComponent
from ReportComposite import ReportComposite


class ReportCompositeTestCase(unittest.TestCase):

    def test_generate_report_component(self):
        mock_component = MagicMock(spec = ReportComponent)
        mock_component.generate_report.return_value = {'data': 'Report 1'}
        mock_component2 = MagicMock(spec =ReportComponent)
        mock_component2.generate_report.return_value = {'data': 'Report 2'}


        composite = ReportComposite()
        composite.add_component(mock_component)
        composite.add_component(mock_component2)

        report_entries = composite.generate_report()

        expected_report_entries = [{'data': 'Report 1'}, {'data': 'Report 2'}]
        self.assertEqual(report_entries, expected_report_entries)

    def test_add_component(self):

        mock_component = MagicMock(spec=ReportComponent)
        composite = ReportComposite()
        composite.add_component(mock_component)

        self.assertIn(mock_component, composite.report_components)

    def test_remove_component(self):

        mock_component = MagicMock(spec=ReportComponent)
        composite = ReportComposite()
        composite.add_component(mock_component)
        composite.remove_component(mock_component)

        self.assertNotIn(mock_component, composite.report_components)