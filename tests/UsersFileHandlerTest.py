import csv
import unittest
from unittest.mock import patch

from UsersFileHandler import UserHandler


class UsersFileHandlerTestCase(unittest.TestCase):


    def setUp(self):
        self.test_file = 'test_users.csv'
        self.user_handler = UserHandler(self.test_file)

    def test_load_user_credentials_from_file(self):
        users = list(self.user_handler.load_user_credentials_from_file())
        self.assertGreater(len(users), 0)
        expected_user = list(users)
        self.assertEqual(users, expected_user)


    @patch('csv.DictReader')
    def test_load_user_credentials_from_file_without_data(self, mock_dict_reader):
        mock_data = []
        mock_dict_reader.return_value = mock_data

        result = self.user_handler.load_user_credentials_from_file()
        self.assertEqual(result, mock_data)
