import csv
import os
import unittest
from UsersFileHandler import UserHandler
from unittest.mock import patch


class UsersFileHandlerTestCase(unittest.TestCase):

    def setUp(self):
        self.test_file = 'test_users.csv'
        self.user_handler = UserHandler(self.test_file)

    def test_load_user_credentials_from_file(self):
        users = list(self.user_handler.load_user_credentials_from_file())

        self.assertGreater(len(users), 0)

        with open(self.test_file, 'r') as file:
            csv_reader = csv.DictReader(file)
            expected_users = [{'User_ID': '1', 'API_KEY': 'key_1'}, {'User_ID': '2', 'API_KEY': 'key_2'}]
            for row, expected_user in zip(csv_reader, expected_users):
                self.assertEqual(row, expected_user)