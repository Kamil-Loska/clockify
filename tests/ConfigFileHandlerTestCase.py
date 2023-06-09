import configparser
import os
import unittest
from configparser import ConfigParser
from unittest.mock import patch

from ConfigFileHandler import ConfigFileHandler


class ConfigFileHandlerTestCase(unittest.TestCase):

    def setUp(self):
        self.mock_config_file = 'mock_config.ini'
        config = configparser.ConfigParser()
        config['Clockify'] = {
            'WORKSPACE_ID': 'valid_id'
        }
        config['FIELDINFO'] = {
            'fullname': 'Imie i nazwisko',
            'data': 'Data',
            'duration-time': 'Czas trwania',
            'description': 'Opis zadania'
        }
        with open(self.mock_config_file, 'w') as configfile:
            config.write(configfile)
        self.config_handler = ConfigFileHandler(self.mock_config_file)

    def test_get_workspace_id(self):
        self.config_handler.config['Clockify'] = {
            'WORKSPACE_ID': 'workspace123'
        }

        result = self.config_handler.get_workspace_id()
        expected_result = 'workspace123'
        self.assertEqual(result, expected_result)

    def test_config_read(self):
        self.config_handler.config['Clockify'] = {
            'WORKSPACE_ID': 'workspace123'
        }

        result = self.config_handler.config.get('Clockify', 'WORKSPACE_ID')
        expected_result = 'workspace123'
        self.assertEqual(result, expected_result)

    def test_translation_mapper(self):
        os.chdir('..')
        expected_report_data = {
            'Fullname': 'John Doe',
            'Date': '2023-05-31',
            'Duration time': '2H 30M',
            'Task description': 'Some task description'
        }

        config_file = 'config.ini'
        real_config_handler = ConfigFileHandler(config_file)
        translation_mapping = self.config_handler.translation_mapper()

        translated_mock_data = {
            translation_mapping.get(key, key): value
            for key, value in expected_report_data.items()
        }

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


