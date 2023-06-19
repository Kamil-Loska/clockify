import unittest
from unittest.mock import MagicMock
from ConfigFileHandler import ConfigFileHandler


class ConfigFileHandlerTestCase(unittest.TestCase):

    def setUp(self):
        self.config_parser_mock = MagicMock()
        self.config_handler = ConfigFileHandler('mock_config.ini')
        self.config_parser_mock.get.return_value = self.config_handler.config.get('Clockify', 'WORKSPACE_ID')

        self.config_parser_mock.return_value = self.config_handler.config['FIELDINFO']

    def test_get_workspace_id(self):
        result = self.config_handler.get_workspace_id()
        expected_result = '123Test'
        self.assertEqual(result, expected_result)

    def test_config_read(self):
        result = self.config_parser_mock.get.return_value
        expected_result = '123Test'
        self.assertEqual(result, expected_result)

    def test_translation_mapper(self):
        result = self.config_handler.translation_mapper()
        expected_result = self.config_handler.config['FIELDINFO']

        self.assertEqual(result, expected_result)

    def test_translation_mapper_invalid(self):
        self.config_parser_mock.__getitem__.return_value['fullName'] = 'Invalid Mapping'

        result = self.config_handler.translation_mapper()

        invalid_result = {
            'fullName': 'Invalid Mapping',
            'date': 'data',
            'durationTime': 'czasTrwania',
            'taskDescription': 'opisZadania'
        }

        self.assertNotEqual(result, invalid_result)
