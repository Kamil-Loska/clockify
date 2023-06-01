import unittest
from unittest.mock import patch, MagicMock
from FileHandler import FileHandler


class FileHandlerTestCase(unittest.TestCase):

    def setUp(self):
        self.file_handler = FileHandler('config.ini')

    @patch('builtins.open')
    @patch('csv.DictReader')
    def test_get_users_from_file(self, mock_dict_reader, mock_open):
        mock_csv_file = MagicMock()
        mock_dict_reader.return_value = mock_csv_file
        mock_csv_file.fieldnames = ['User1_Id', 'API1', 'User2_Id', 'API2']
        mock_csv_file.__iter__.return_value = [
            {'User1_Id': '123', 'API1': 'api_key_1', 'User2_Id': '456', 'API2': 'api_key_2'}
        ]
        result = self.file_handler.get_users_from_file()

        mock_open.assert_called_once_with('Users.csv', 'r')
        mock_dict_reader.assert_called_once_with(mock_open.return_value.__enter__.return_value)
        self.assertEqual(result, {'123': 'api_key_1'})

    def test_translation_mapper(self):
        self.file_handler.config['FIELDINFO'] = {
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

        translation_mapping = self.file_handler.translation_mapper()
        translated_data = {
            translation_mapping.get(key, key): value
            for key, value in report_data.items()
        }

        self.assertNotEqual(translated_data, expected_translation)


if __name__ == '__main__':
    unittest.main()
