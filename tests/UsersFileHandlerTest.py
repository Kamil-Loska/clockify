import csv
import os
import unittest
from UsersFileHandler import UserHandler
from unittest.mock import patch


class UsersFileHandlerTestCase(unittest.TestCase):

    def setUp(self):
        self.test_file = 'test_users.csv'
        with open(self.test_file, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['User_ID', 'API_KEY'])
            writer.writeheader()
            writer.writerow({'User_ID': '1', 'API_KEY': 'key_1'})
            writer.writerow({'User_ID': '2', 'API_KEY': 'key_2'})

    def tearDown(self):
        os.remove(self.test_file)

    def test_load_user_credentials_from_file(self):
        user_handler = UserHandler(self.test_file)

        with patch('builtins.open', return_value=open(self.test_file, 'r')) as mock_file:
            users = user_handler.load_user_credentials_from_file()

            mock_file.assert_called_once_with(self.test_file, 'r')

            self.assertGreater(len(users), 0)

            api_key, user_id = users[0]
            self.assertEqual(api_key, 'key_1')
            self.assertEqual(user_id, '1')

            api_key, user_id = users[1]
            self.assertEqual(api_key, 'key_2')
            self.assertEqual(user_id, '2')
