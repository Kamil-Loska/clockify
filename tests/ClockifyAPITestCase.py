import unittest
from unittest.mock import MagicMock, patch
import pytest as pytest
from ClockifyAPI import ClockifyAPI
from User import User


class ClockifyAPITestCase(unittest.TestCase):

    @pytest.fixture
    def mock_get_request(self):
        with patch('ClockifyAPI.requests.get') as mock_get:
            yield mock_get

    def setUp(self):
        self.workspace_id = 'workspace_id'
        self.clockify_api = ClockifyAPI(self.workspace_id)
        self.user_credentials = User('User_ID', 'API_KEY')

    def create_mock_response(self, data, status_code=200):
        mock_response = MagicMock()
        mock_response.json.return_value = data
        mock_response.status_code = status_code
        return mock_response

    @patch('ClockifyAPI.requests.get')
    def test_get_time_entries_per_user(self, mock_get):
        mock_response1 = self.create_mock_response([
            [{'data': 'response1'}, {'data': 'response2'}, {'data': 'response3'}],
            [{'data': 'response4'}, {'data': 'response5'}],
            [],
        ])
        mock_response2 = self.create_mock_response([])
        mock_get.side_effect = [mock_response1, mock_response2]

        actual_result = self.clockify_api.get_time_entries_per_user(self.user_credentials, '2023-05-15', '2023-05-16')

        expected_result = [
            [{'data': 'response1'}, {'data': 'response2'}, {'data': 'response3'}],
            [{'data': 'response4'}, {'data': 'response5'}],
            [],
        ]

        self.assertEqual(actual_result, expected_result)

    @patch('requests.get')
    def test_get_user_name_client_error(self, mock_get):
        mock_get.return_value = MagicMock(status_code=403)

        # Call the method and check if it raises an exception
        with self.assertRaises(Exception):
            self.clockify_api.get_user_name('invalid_api_key')



    #API ZWRACA NATURALNE DANE, czyli 3 2 1 odpowiedzi z response'a.

    @patch('ClockifyAPI.requests.get')
    def test_get_time_entries_per_user_with_empty_response(self, mock_get):
        mock_responses = [
            self.create_mock_response([{'data': 'response1'}, {'data': 'response2'}, {'data': 'response3'}]),
            self.create_mock_response([]),
            self.create_mock_response([{'data': 'response4'}, {'data': 'response5'}]),
        ]
        mock_get.side_effect = mock_responses

        actual_result = self.clockify_api.get_time_entries_per_user(self.user_credentials, '2023-05-15', '2023-05-16')

        expected_result = [
            {'data': 'response1'},
            {'data': 'response2'},
            {'data': 'response3'},
        ]

        self.assertEqual(actual_result, expected_result)

    @patch('ClockifyAPI.requests.get')
    def test_get_user_credentials_with_missing_name(self, mock_get_request):
        mock_response = self.create_mock_response({'name': ''})
        mock_get_request.return_value = mock_response

        result = self.clockify_api.get_user_name(self.user_credentials.api_key)

        mock_get_request.assert_called_once_with('https://api.clockify.me/api/v1/user',
                                                 headers={'X-Api-Key': 'API_KEY', 'Content-Type': 'application/json'},
                                                 params=None)
        expected_result = ''
        self.assertEqual(result, expected_result)
