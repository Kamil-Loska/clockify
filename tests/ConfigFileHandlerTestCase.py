import unittest
from configparser import ConfigParser
from unittest.mock import MagicMock
from ConfigFileHandler import ConfigFileHandler


class ConfigFileHandlerTestCase(unittest.TestCase):

    def setUp(self):
        self.config_parser_mock = MagicMock(spec=ConfigParser)
        self.config_handler = ConfigFileHandler('mock_config.ini')

    def test_get_workspace_id(self):
        result = self.config_handler.get_workspace_id()
        expected_result = '123Test'
        self.assertEqual(result, expected_result)

    def test_translation_mapper(self):
        self.config_parser_mock.__getitem__.return_value = {
            'fullName': 'imieNazwisko',
            'date': 'data',
            'durationTime': 'czasTrwania',
            'taskDescription': 'opisZadania'
        }
        result = self.config_handler.translation_mapper()
        expected_result = {
            'fullName': 'imieNazwisko',
            'date': 'data',
            'durationTime': 'czasTrwania',
            'taskDescription': 'opisZadania'
        }
        self.assertEqual(result, expected_result)

    def test_translation_mapper_unknown_field(self):
        result = self.config_handler.translation_mapper()
        self.assertNotIn('position', result)

    def test_add_new_field(self):
        self.config_handler.config['FIELDINFO']['position'] = 'Position'
        result = self.config_handler.translation_mapper()
        expected_result = {
            'fullName': 'Invalid Mapping',
            'date': 'data',
            'durationTime': 'czasTrwania',
            'taskDescription': 'opisZadania'
        }
        self.assertNotEqual(result, expected_result)
