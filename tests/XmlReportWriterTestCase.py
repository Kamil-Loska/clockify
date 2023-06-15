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
                'date': '2023-05-15',
                'durationTime': '1H30M',
                'taskDescription': 'Task 1'
            },
            {
                'fullName': 'Jane Doe',
                'date': '2023-05-15',
                'durationTime': '2H',
                'taskDescription': 'Task 2'
            },
        ]

        writer.write(report_entries)

        mock_open.assert_called_once_with('report.xml', 'w')

        handle = mock_open()
        self.assertIn('<ClockifyReport fullName="John Doe" date="2023-05-15" durationTime="1H30M"'
                      ' taskDescription="Task 1"/>', handle.write.call_args_list[0][0][0])

        self.assertIn('<ClockifyReport fullName="Jane Doe" date="2023-05-15" durationTime="2H"'
                      ' taskDescription="Task 2"/>', handle.write.call_args_list[0][0][0])