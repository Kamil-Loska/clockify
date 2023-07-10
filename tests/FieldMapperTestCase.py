import unittest
from unittest.mock import MagicMock

from ConfigFileHandler import ConfigFileHandler
from FieldMapper import FieldMapper


class FieldMapperTestCase(unittest.TestCase):

    def setUp(self):
        self.mock_config_handler = ConfigFileHandler('mock_config.ini')
        self.field_mapper = FieldMapper(self.mock_config_handler)

    def test_map_fields(self):
        report_entries = [{'fullName': 'John Doe', 'date': '2023-05-15'}]

        mapped_report_data = list(self.field_mapper.map_fields(report_entries))

        expected_report_data = [{'imieNazwisko': 'John Doe', 'data': '2023-05-15'}]
        self.assertEqual(mapped_report_data, expected_report_data)





