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
        mock_responses = [
            self.create_mock_response([{'data': 'response1'}, {'data': 'response2'}, {'data': 'response3'}]),
            self.create_mock_response([{'data': 'response4'}, {'data': 'response5'}]),
            self.create_mock_response([]),
        ]
        mock_get.side_effect = mock_responses

        actual_result = self.clockify_api.get_time_entries_per_user(self.user_credentials, '2023-05-15', '2023-05-16')

        expected_result = [
            {'data': 'response1'},
            {'data': 'response2'},
            {'data': 'response3'},
            {'data': 'response4'},
            {'data': 'response5'},
        ]
        self.assertEqual(actual_result, expected_result)

    @patch('ClockifyAPI.requests.get')
    def test_get_user_name(self, mock_get):
        expected_name = 'Test User'
        mock_response = self.create_mock_response({'name': expected_name})
        mock_get.return_value = mock_response

        actual_name = self.clockify_api.get_user_name(self.user_credentials.api_key)

        self.assertEqual(actual_name, expected_name)
