import unittest
from unittest.mock import patch, MagicMock
from UsersFileHandler import UserHandler


class UsersFileHandlerTestCase(unittest.TestCase):

    @patch('builtins.open')
    @patch('csv.DictReader')
    def test_get_users_from_file(self, mock_dict_reader, mock_open):
        user_handler = UserHandler('Users.csv')
        mock_csv_file = MagicMock()
        mock_dict_reader.return_value = mock_csv_file
        mock_csv_file.fieldnames = ['User_ID', 'API_KEY']
        mock_csv_file.__iter__.return_value = [
            {'User_ID': '123', 'API_KEY': 'api_key_1'},
            {'User_ID': '456', 'API_KEY': 'api_key_2'},
            {'User_ID': '789', 'API_KEY': 'api_key_3'}
        ]
        result = user_handler.load_user_credentials_from_file()

        mock_open.assert_called_once_with('Users.csv', 'r')
        mock_dict_reader.assert_called_once_with(mock_open.return_value.__enter__.return_value)

        expected_result = {
            '123': 'api_key_1',
            '456': 'api_key_2',
            '789': 'api_key_3'
        }
        self.assertEqual(result, expected_result)
