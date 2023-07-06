import unittest
from unittest.mock import patch
from XmlReportWriter import XmlReportWriter


class XmlReportWriterTest(unittest.TestCase):

    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_write(self, mock_open):
        writer = XmlReportWriter()
        report_entries = [
            {
                'fullName': 'John Doe',
                'department': 'IT Security',
                'date': '2023-05-15',
                'durationTime': '1H30M',
                'taskDescription': 'Task 1'
            },
            {
                'fullName': 'John Doe',
                'department': 'Testing',
                'date': '2023-05-15',
                'durationTime': '2H',
                'taskDescription': 'Task 2'
            },
        ]

        writer.write_report(report_entries)

        mock_open.assert_called_once_with('report.xml', 'w')

        self.assertIn(
            '<ClockifyReport fullName="John Doe" department="IT Security" date="2023-05-15" durationTime="1H30M"'
            ' taskDescription="Task 1"/>', mock_open().write.call_args_list[0][0][0])

        self.assertIn('<ClockifyReport fullName="Jane Doe" department="Testing" date="2023-05-15" durationTime="2H"'
                      ' taskDescription="Task 2"/>', mock_open().write.call_args_list[0][0][0])
