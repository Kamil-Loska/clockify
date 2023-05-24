from unittest import mock
import sys
import pytest
from main import ClockifyApp

from unittest.mock import patch


class TestClockifyApp:

    @pytest.fixture
    def clockify(self):
        return ClockifyApp()

    @pytest.fixture
    def mock_get_request(self):
        with patch('main.requests.get') as mock_get:
            yield mock_get

    def test_validate_date_format_valid_dates(self, clockify):
        assert clockify.validate_date_format("2023-05-14", "2023-05-16") is True
        assert clockify.validate_date_format("2023-01-01", "2023-12-12") is True

    def test_validate_date_format_invalid_dates(self, clockify):
        assert clockify.validate_date_format("14-05-2023", "16-05-2023") is False
        assert clockify.validate_date_format("2023 05 14", "2023 05 12") is False
        assert clockify.validate_date_format("2023/05/14", "2023-05-16") is False

    def test_validate_date_format_invalid_year(self, clockify):
        assert clockify.validate_date_format("2023-05-14", "20023-12-03") is False
        assert clockify.validate_date_format("0000-05-10", "2023-05-23") is False
        assert clockify.validate_date_format("1212-05-03", "4444-05-10") is False
        assert clockify.validate_date_format("23-12-01", ".23-12-31") is False

    def test_validate_date_format_invalid_month(self, clockify):
        assert clockify.validate_date_format("2023-15-14", "2023-12-03") is False
        assert clockify.validate_date_format("2023-00-10", "2023-05-23") is False
        assert clockify.validate_date_format("2023-30-03", "2023-05-10") is False

    def test_validate_date_format_invalid_day(self, clockify):
        assert clockify.validate_date_format("2023-02-29", "2023-12-03") is False
        assert clockify.validate_date_format("2023-05-00", "2023-05-23") is False
        assert clockify.validate_date_format("2023-05-32", "2023-05-2023") is False

    def test_format_duration(self, clockify):
        assert clockify.format_duration(None) == None
        assert clockify.format_duration("PT2H30M") == "2H 30M"
        assert clockify.format_duration("PT1M30S") == "1M 30S"
        assert clockify.format_duration("PT3H45S") == "3H 45S"
        assert clockify.format_duration("PT2H") == "2H"
        assert clockify.format_duration("PT45M") == "45M"
        assert clockify.format_duration("PT30S") == "30S"

    @mock.patch('main.requests.get')
    def test_send_get_request(self, mock_get_request, clockify):
        mock_response = mock.MagicMock()
        expected_response = {'id': '123', 'description': 'Test Result'}
        mock_response.json.return_value = expected_response
        mock_get_request.return_value = mock_response

        endpoint = 'test-endpoint'
        params = {'key': 'value'}
        result = clockify.send_get_request(endpoint, params=params)

        mock_get_request.assert_called_with(clockify.BASE_URL + endpoint, headers=mock.ANY, params=params)

        assert result == expected_response

    @mock.patch('main.requests.get')
    def test_generate_raport_iteration_count(self, mock_send_get_request):
        mock_responses = [
            [{'data': 'response1'}, {'data': 'response2'}],
            [{'data': 'response3'}, {'data': 'response4'}, {'data': 'response5'}]
        ]

        mock_send_get_request.json.side_effect = mock_responses
        clockify = ClockifyApp()
        clockify.generate_raport('2023-05-15', '2023-05-16')

        expected_iterations = len(mock_responses)
        actual_iterations = mock_send_get_request.call_count

        assert expected_iterations == actual_iterations