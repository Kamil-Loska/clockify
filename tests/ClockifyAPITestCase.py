import unittest
from unittest.mock import MagicMock, patch
import pytest as pytest
import requests

from ClockifyAPI import ClockifyAPI


class ClockifyAPITestCase(unittest.TestCase):

    @pytest.fixture
    def mock_get_request(self):
        with patch('ClockifyAPI.requests.get') as mock_get:
            yield mock_get

    def setUp(self):
        self.clockify_api = ClockifyAPI(workspace_id='workspace_id')
        self.user_credentials = {'User_ID': '456', 'API_KEY': 'API_KEY'}

    def create_mock_response(self, data):
        mock_response = MagicMock()
        mock_response.json.return_value = data
        return mock_response

    @patch('ClockifyAPI.requests.get')
    def test_send_get_request(self, mock_get):
        endpoint = f'workspaces/123/user/{self.user_credentials["User_ID"]}/time-entries'
        params = {'start': '2023-05-15T00:00:00Z', 'end': '2023-05-16T23:59:59Z'}

        mock_response = self.create_mock_response({'data': 'response_data'})
        mock_get.return_value = mock_response

        clockify_api = ClockifyAPI(self.user_credentials["API_KEY"])
        response = clockify_api._send_get_request(self.user_credentials["API_KEY"], endpoint, params)
        self.assertEqual(response, {'data': 'response_data'})

    @patch('ClockifyAPI.requests.get')
    def test_get_time_entries_per_user(self, mock_get_request):
        mock_responses = [
            [{'data': 'response1'}, {'data': 'response2'}, {'data': 'response3'}],
            [{'data': 'response4'}, {'data': 'response5'}],
            [],
        ]
        self.clockify_api._send_get_request = MagicMock(side_effect=mock_responses)
        result = self.clockify_api.get_time_entries_per_user(self.user_credentials,
                                                             '2023-05-15', '2023-05-16')

        expected_result = [
            {'data': 'response1'},
            {'data': 'response2'},
            {'data': 'response3'},
            {'data': 'response4'},
            {'data': 'response5'},
        ]
        self.assertEqual(result, expected_result)

    @patch('ClockifyAPI.requests.get')
    def test_get_user_data(self, mock_get_request):
        mock_response = self.create_mock_response({'name': 'John Doe'})
        mock_get_request.return_value = mock_response

        result = self.clockify_api.get_user_name({'API_KEY': 'API_KEY'})

        self.assertEqual(result, 'John Doe')

    @patch('ClockifyAPI.requests.get')
    def test_send_get_request_with_invalid_url(self, mock_get):
        endpoint = 'invalid_endpoint'
        params = {'start': '2023-05-15T00:00:00Z', 'end': '2023-05-16T23:59:59Z'}
        mock_response = self.create_mock_response({'data': 'response_data'})
        mock_get.return_value = mock_response

        clockify_api = ClockifyAPI(self.user_credentials["API_KEY"])
        response = clockify_api._send_get_request(self.user_credentials["API_KEY"], endpoint, params)
        self.assertEqual(response, {'data': 'response_data'})

    @patch('ClockifyAPI.requests.get')
    def test_get_time_entries_per_user_with_empty_response(self, mock_get_request):
        mock_responses = [
            [{'data': 'response1'}, {'data': 'response2'}, {'data': 'response3'}],
            [],
            [{'data': 'response4'}, {'data': 'response5'}],
        ]
        self.clockify_api.send_get_request = MagicMock(side_effect=mock_responses)
        result = self.clockify_api.get_time_entries_per_user(self.user_credentials,
                                                             '2023-05-15', '2023-05-16')
        expected_result = []
        self.assertEqual(result, expected_result)

    @patch('ClockifyAPI.requests.get')
    def test_get_user_credentials_with_missing_name(self, mock_get_request):
        mock_response = self.create_mock_response({'name': ''})
        mock_get_request.return_value = mock_response

        result = self.clockify_api.get_user_name({'API_KEY': 'API_KEY'})

        mock_get_request.assert_called_once_with('https://api.clockify.me/api/v1/user',
                                                 headers={'X-Api-Key': 'API_KEY', 'Content-Type': 'application/json'},
                                                 params=None)
        expected_result = ''
        self.assertEqual(result, expected_result)
