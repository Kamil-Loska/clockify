import unittest
from unittest.mock import MagicMock, patch

from ConfigFileHandler import ConfigFileHandler


class ConfigFileHandlerTestCase(unittest.TestCase):

    def setUp(self):
        self.config_parser_mock = MagicMock()
        self.config_parser_mock.get.return_value = '123Test'
        self.config_parser_mock.__getitem__.return_value = {
            'fullName': 'imieNazwisko',
            'date': 'data',
            'durationTime': 'czasTrwania',
            'taskDescription': 'opisZadania'
        }

        with patch('configparser.ConfigParser', return_value=self.config_parser_mock):
            self.config_handler = ConfigFileHandler('mock_config.ini')

    def test_get_workspace_id(self):
        result = self.config_handler.get_workspace_id()
        expected_result = '123Test'
        self.assertEqual(result, expected_result)

    def test_config_read(self):
        result = self.config_handler.config.get('Clockify', 'WORKSPACE_ID')
        expected_result = '123Test'
        self.assertEqual(result, expected_result)

    def test_translation_mapper(self):
        result = self.config_handler.translation_mapper()
        expected_result = {
            'fullName': 'imieNazwisko',
            'date': 'data',
            'durationTime': 'czasTrwania',
            'taskDescription': 'opisZadania'
        }

        self.assertEqual(result, expected_result)

    def test_translation_mapper_invalid(self):
        self.config_parser_mock.__getitem__.return_value['fullName'] = 'Invalid Mapping'

        result = self.config_handler.translation_mapper()

        expected_result = {
            'fullName': 'Invalid Mapping',
            'date': 'data',
            'durationTime': 'czasTrwania',
            'taskDescription': 'opisZadania'
        }

        self.assertDictEqual(result, expected_result)
