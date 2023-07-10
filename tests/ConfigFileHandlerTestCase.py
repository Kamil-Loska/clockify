import unittest
from ConfigFileHandler import ConfigFileHandler


class ConfigFileHandlerTestCase(unittest.TestCase):

    def setUp(self):
        self.config_handler = ConfigFileHandler('mock_config.ini')

    def test_get_workspace_id(self):
        result = self.config_handler.get_workspace_id()
        expected_result = '123Test'
        self.assertEqual(result, expected_result)

    def test_translation_mapper(self):
        expected_values = {
            'fullName': 'imieNazwisko',
            'date': 'data',
            'durationTime': 'czasTrwania',
            'taskDescription': 'opisZadania'
        }
        result = self.config_handler.translation_mapper()

        self.assertEqual(result, expected_values)

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
