import configparser
import os
import unittest

from ConfigFileHandler import ConfigFileHandler


class ConfigFileHandlerTestCase(unittest.TestCase):

    def setUp(self):
        self.config_handler = ConfigFileHandler('mock_config.ini')

    def test_get_workspace_id(self):
        result = self.config_handler.get_workspace_id()
        expected_result = 'valid_id'
        self.assertEqual(result, expected_result)

    def test_config_read(self):
        result = self.config_handler.config.get('Clockify', 'WORKSPACE_ID')
        expected_result = 'valid_id'
        self.assertEqual(result, expected_result)

    def test_translation_mapper(self):
        os.chdir('..')
        expected_report_data = {
            'Fullname': 'John Doe',
            'Date': '2023-05-31',
            'Duration-time': '2H 30M',
            'Task-description': 'Some task description'
        }

        translation_mapping = self.config_handler.translation_mapper()

        translated_mock_data = {
            translation_mapping.get(key, key): value
            for key, value in expected_report_data.items()
        }

        config_file = 'config.ini'
        real_config_handler = ConfigFileHandler(config_file)

        translated_data = {
            real_config_handler.translation_mapper().get(key, key): value
            for key, value in expected_report_data.items()
        }

        self.assertEqual(translated_mock_data, translated_data)

    def test_translation_mapper_invalid(self):
        self.config_handler.config['FIELDINFO']['fullname'] = 'Invalid Mapping'
        result = self.config_handler.translation_mapper()
        expected_result = {
            'Invalid Mapping': 'Invalid Mapping',
            'Data': 'Data',
            'Czas trwania': 'Czas trwania',
            'Opis zadania': 'Opis zadania'
        }

        self.assertEqual(result, expected_result)
