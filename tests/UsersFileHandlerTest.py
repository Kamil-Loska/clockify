import csv
import unittest
from UsersFileHandler import UserHandler


class UsersFileHandlerTestCase(unittest.TestCase):

    def setUp(self):
        self.test_file = 'test_users.csv'
        self.user_handler = UserHandler(self.test_file)

    def test_load_user_credentials_from_file(self):
        users = self.user_handler.load_user_credentials_from_file()
        self.assertGreater(len(users), 0)

        with open(self.test_file, 'r') as file:
            csv_reader = csv.DictReader(file)
            expected_users = list(csv_reader)

            self.assertEqual(users, expected_users)
