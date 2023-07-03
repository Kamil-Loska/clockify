import unittest
from configparser import ConfigParser
from unittest.mock import MagicMock
from ConfigFileHandler import ConfigFileHandler


class ConfigFileHandlerTestCase(unittest.TestCase):

    def setUp(self):
        self.config_parser_mock = MagicMock(spec=ConfigParser)

        self.config_handler = ConfigFileHandler('mock_config.ini')
        self.config_handler.config = self.config_parser_mock

    def test_get_workspace_id(self):
        self.config_parser_mock.get.return_value = '123Test'
        result = self.config_handler.get_workspace_id()
        expected_result = '123Test'
        self.assertEqual(result, expected_result)

    def test_translation_mapper(self):
        expected_result = {
            'fullName': 'imieNazwisko',
            'date': 'data',
            'durationTime': 'czasTrwania',
            'taskDescription': 'opisZadania'
        }

        self.config_parser_mock.__getitem__.return_value = expected_result

        result = self.config_handler.translation_mapper()
        self.assertEqual(result, expected_result)

    def test_translation_mapper_ignores_unknown_field(self):
        config_values = {
            'fullName': 'imieNazwisko',
            'date': 'data',
            'durationTime': 'czasTrwania',
            'taskDescription': 'opisZadania',
            'position': 'UnknownPosition'
        }

        result = self.config_handler.translation_mapper()
        self.assertNotEquals(config_values, result)
