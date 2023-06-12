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
        result = self.config_handler.translation_mapper()
        expected_result = {
            'Fullname': 'Imie-i-nazwisko',
            'Date': 'Data',
            'Duration-time': 'Czas-trwania',
            'Task-description': 'Opis-zadania'
        }

        result_lower = {k.lower(): v for k, v in result.items()}
        expected_result_lower = {k.lower(): v for k, v in expected_result.items()}

        self.assertEqual(result_lower, expected_result_lower)


    def test_translation_mapper_invalid(self):
        self.config_handler.config['FIELDINFO']['Fullname'] = 'Invalid Mapping'

        result = self.config_handler.translation_mapper()

        expected_result = {
            'Fullname': 'Invalid Mapping',
            'Date': 'Data',
            'Duration-Time': 'Czas-trwania',
            'Task-Description': 'Opis-zadania'
        }
        sorted_result = {k.title(): v for k, v in result.items()}
        self.assertDictEqual(sorted_result, expected_result)








