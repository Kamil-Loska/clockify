import unittest
from configparser import ConfigParser
from unittest.mock import MagicMock
from ConfigFileHandler import ConfigFileHandler


class ConfigFileHandlerTestCase(unittest.TestCase):

    def setUp(self):
        self.config_parser_mock = MagicMock(spec=ConfigParser)
        self.config_handler = ConfigFileHandler('mock_config.ini')

    def test_get_workspace_id(self):
        self.config_parser_mock.get.return_value = '123Test'
        result = self.config_handler.get_workspace_id()
        expected_result = '123Test'
        self.assertEqual(result, expected_result)

    def test_translation_mapper(self):
        expected_values = {
            'fullName': 'imieNazwisko',
            'department': 'dzial',
            'date': 'data',
            'durationTime': 'czasTrwania',
            'taskDescription': 'opisZadania'
        }
        result = self.config_handler.translation_mapper()

        self.assertEqual(result['fullName'], expected_values['fullName'])
        self.assertEqual(result['department'], expected_values['department'])
        self.assertEqual(result['date'], expected_values['date'])
        self.assertEqual(result['durationTime'], expected_values['durationTime'])
        self.assertEqual(result['taskDescription'], expected_values['taskDescription'])

    def test_translation_mapper_ignores_unknown_field(self):
        config_values = {
            'fullName': 'imieNazwisko',
            'departamnt': 'Support',
            'date': 'data',
            'durationTime': 'czasTrwania',
            'taskDescription': 'opisZadania',
            'position': 'UnknownPosition'
        }

        result = self.config_handler.translation_mapper()
        self.assertNotEquals(config_values, result)
