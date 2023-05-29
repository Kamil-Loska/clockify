from unittest import mock
import pytest
from ClockifyReportGenerator import ClockifyReportGenerator
from Argument_provider import ArgumentProvider
from unittest.mock import patch, MagicMock


class TestClockifyApp:

    @pytest.fixture
    def argument_provider(self):
        return ArgumentProvider()

    @pytest.fixture
    def mock_get_request(self):
        with patch('ClockifyReportGenerator.requests.get') as mock_get:
            yield mock_get

    def test_validate_date_format_valid_dates(self, argument_provider):
        assert argument_provider.validate_date_format("2023-05-14", "2023-05-16") is True
        assert argument_provider.validate_date_format("2023-01-01", "2023-12-12") is True

    def test_validate_date_format_invalid_dates(self, argument_provider):
        assert argument_provider.validate_date_format("14-05-2023", "16-05-2023") is False
        assert argument_provider.validate_date_format("2023 05 14", "2023 05 12") is False
        assert argument_provider.validate_date_format("2023/05/14", "2023-05-16") is False

    def test_validate_date_format_invalid_year(self, argument_provider):
        assert argument_provider.validate_date_format("2023-05-14", "20023-12-03") is False
        assert argument_provider.validate_date_format("0000-05-10", "2023-05-23") is False
        assert argument_provider.validate_date_format("1212-05-03", "4444-05-10") is False
        assert argument_provider.validate_date_format("23-12-01", ".23-12-31") is False

    def test_validate_date_format_invalid_month(self, argument_provider):
        assert argument_provider.validate_date_format("2023-15-14", "2023-12-03") is False
        assert argument_provider.validate_date_format("2023-00-10", "2023-05-23") is False
        assert argument_provider.validate_date_format("2023-30-03", "2023-05-10") is False

    def test_validate_date_format_invalid_day(self, argument_provider):
        assert argument_provider.validate_date_format("2023-02-29", "2023-12-03") is False
        assert argument_provider.validate_date_format("2023-05-00", "2023-05-23") is False
        assert argument_provider.validate_date_format("2023-05-32", "2023-05-2023") is False

    def test_format_duration(self, argument_provider):
        assert argument_provider.format_duration(None) == None
        assert argument_provider.format_duration("PT2H30M") == "2H 30M"
        assert argument_provider.format_duration("PT1M30S") == "1M 30S"
        assert argument_provider.format_duration("PT3H45S") == "3H 45S"
        assert argument_provider.format_duration("PT2H") == "2H"
        assert argument_provider.format_duration("PT45M") == "45M"
        assert argument_provider.format_duration("PT30S") == "30S"

    @mock.patch('main.requests.get')
    def test_send_get_request(self, mock_get_request, argument_provider):
        mock_response = mock.MagicMock()
        expected_response = {'id': '123', 'description': 'Test Result'}
        mock_response.json.return_value = expected_response
        mock_get_request.return_value = mock_response

        endpoint = 'test-endpoint'
        params = {'key': 'value'}
        result = argument_provider.send_get_request(endpoint, params=params)

        mock_get_request.assert_called_with(argument_provider.BASE_URL + endpoint, headers=mock.ANY, params=params)

        assert result == expected_response

    @mock.patch('ClockifyAPI.requests.get')
    def test_generate_raport_iteration_count(self, mock_get_request):
        mock_responses = [
            [{'data': 'response1'}, {'data': 'response2'}, {'data': 'response3'}],
            [{'data': 'response4'}, {'data': 'response5'}],
            [],
        ]

        mock_get_request.return_value = MagicMock()
        mock_get_request.return_value.side_effect = mock_responses
        clockify_app = ClockifyReportGenerator()

        clockify_app.generate_raport('2023-05-15', '2023-05-16')

        assert mock_get_request.call_count == 4
