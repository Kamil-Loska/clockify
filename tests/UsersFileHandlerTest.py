import unittest
from UsersFileHandler import UserHandler


class UsersFileHandlerTestCase(unittest.TestCase):

    def setUp(self):
        self.test_file = 'test_users.csv'
        self.user_handler = UserHandler(self.test_file)

    def test_load_user_credentials_from_file(self):
        users = list(self.user_handler.load_user_credentials_from_file())
        self.assertEqual(len(users), 2)

        first_user = users[0]
        self.assertEqual(first_user.user_id, '1')
        self.assertEqual(first_user.api_key, 'key_1')

        second_user = users[1]
        self.assertEqual(second_user.user_id, '2')
        self.assertEqual(second_user.api_key, 'key_2')

    def test_file_non_exists(self):
        user_handler = UserHandler('test_user.csv')
        with self.assertRaises(FileNotFoundError):
            user_handler.load_user_credentials_from_file()
