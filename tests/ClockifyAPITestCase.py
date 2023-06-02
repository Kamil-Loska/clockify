import unittest
import pytest
from unittest.mock import MagicMock, patch
from ClockifyAPI import ClockifyAPI


class ClockifyAPITestCase(unittest.TestCase):

    @pytest.fixture
    def mock_get_request(self):
        with patch('ClockifyAPI.requests.get') as mock_get:
            yield mock_get

    def setUp(self):
        self.clockify_api = ClockifyAPI(workspace_id='workspace_id')

    @patch('UsersFileHandler.UserHandler.load_user_credentials')
    @patch('ClockifyAPI.requests.get')
    def test_send_get_request(self, mock_get, mock_load_user_credentials):
        users_credentials = {'456': 'API_KEY'}
        mock_load_user_credentials.return_value = users_credentials

        endpoint = 'workspaces/123/user/456/time-entries'
        params = {'start': '2023-05-15T00:00:00Z', 'end': '2023-05-16T23:59:59Z'}
        expected_url = 'https://api.clockify.me/api/v1/' + endpoint
        expected_headers = {
            'X-Api-Key': 'API_KEY',
            'Content-Type': 'application/json'
        }
        mock_response = MagicMock()
        mock_response.json.return_value = {'data': 'response_data'}
        mock_get.return_value = mock_response

        clockify_api = ClockifyAPI('123')
        response = clockify_api.send_get_request('API_KEY', endpoint, params)

        mock_get.assert_called_once_with(expected_url, headers=expected_headers, params=params)
        self.assertEqual(response, {'data': 'response_data'})

    @patch('ClockifyAPI.requests.get')
    def test_get_time_entries_per_user(self, mock_get_request):
        expected_endpoint = 'workspaces/workspace_id/user/USER_ID/time-entries'
        expected_params = {'start': '2023-05-15T00:00:00Z', 'page': 3, 'end': '2023-05-16T23:59:59Z'}
        mock_responses = [
            [{'data': 'response1'}, {'data': 'response2'}, {'data': 'response3'}],
            [{'data': 'response4'}, {'data': 'response5'}],
            [],
        ]
        self.clockify_api.send_get_request = MagicMock(side_effect=mock_responses)
        result = self.clockify_api.get_time_entries_per_user('API_KEY', 'USER_ID', '2023-05-15', '2023-05-16')
        expected_result = [
            {'data': 'response1'},
            {'data': 'response2'},
            {'data': 'response3'},
            {'data': 'response4'},
            {'data': 'response5'},

        ]
        self.clockify_api.send_get_request.assert_called_with('API_KEY', expected_endpoint, expected_params)
        self.assertEqual(result, expected_result)

    @patch('ClockifyAPI.ClockifyAPI.send_get_request')
    def test_get_user_data(self, mock_get_request):
        mock_response = {'name': 'John Doe'}
        mock_get_request.return_value = mock_response

        result = self.clockify_api.get_user_name('API_KEY')

        mock_get_request.assert_called_once_with('API_KEY', 'user')
        self.assertEqual(result, 'John Doe')
