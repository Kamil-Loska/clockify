import unittest
from ConfigFileHandler import ConfigFileHandler


class UsersFileHandlerTestCase(unittest.TestCase):

    def setUp(self):
        self.config_handler = ConfigFileHandler('config.ini')

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
        self.config_handler.config['FIELDINFO'] = {
            'field1': 'Imie i nazwisko',
            'field2': 'Data',
            'field3': 'Czas trwania',
            'field4': 'Opis zadania'
        }

        report_data = {
            'Fullname': 'John Doe',
            'Date': '2023-05-31',
            'Duration time': '2H 30M',
            'Task description': 'Some task description'
        }

        expected_translation = {
            'Imie i nazwisko': 'John Doe',
            'Data': '2023-05-31',
            'Czas trwania': '2H 30M',
            'Opis zadania': 'Some task description'
        }

        translation_mapping = self.config_handler.translation_mapper()
        translated_data = {
            translation_mapping.get(key, key): value
            for key, value in report_data.items()
        }

        self.assertNotEqual(translated_data, expected_translation)
