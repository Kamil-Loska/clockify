from unittest import mock
import pytest
from ClockifyAPI import ClockifyAPI
from ClockifyReportGenerator import ClockifyReportGenerator
from Argument_provider import ArgumentProvider
from unittest.mock import patch, MagicMock


class TestClockifyApp:
    @pytest.fixture
    def argument_provider(self):
        return ArgumentProvider()

    @pytest.fixture
    def mock_get_request(self):
        with patch('ClockifyAPI.requests.get') as mock_get:
            yield mock_get

    @pytest.fixture
    def clockify_report_generator(self):
        return ClockifyReportGenerator()

    @pytest.fixture
    def clockify_api(self):
        return ClockifyAPI()

    def test_validate_date_format_valid_dates(self, argument_provider):
        assert argument_provider.validate_date_format("2023-05-14", "2023-05-16") is True
        assert argument_provider.validate_date_format("2023-01-01", "2023-12-12") is True

    def test_validate_date_format_invalid_dates(self, argument_provider):
        assert argument_provider.validate_date_format("14-05-2023", "16-05-2023") is False
        assert argument_provider.validate_date_format("2023 05 14", "2023 05 12") is False
        assert argument_provider.validate_date_format("2023/05/14", "2023-05-16") is False

    def test_validate_date_format_invalid_year(self, argument_provider):
        assert argument_provider.validate_date_format("20023-05-14", "20023-12-03") is False
        assert argument_provider.validate_date_format("23-12-01", ".23-12-31") is False

    def test_validate_date_format_invalid_month(self, argument_provider):
        assert argument_provider.validate_date_format("2023-15-14", "2023-12-03") is False
        assert argument_provider.validate_date_format("2023-00-10", "2023-05-23") is False
        assert argument_provider.validate_date_format("2023-30-03", "2023-05-10") is False

    def test_validate_date_format_invalid_day(self, argument_provider):
        assert argument_provider.validate_date_format("2023-02-29", "2023-12-03") is False
        assert argument_provider.validate_date_format("2023-05-00", "2023-05-23") is False
        assert argument_provider.validate_date_format("2023-05-32", "2023-05-2023") is False

    def test_format_duration(self, clockify_report_generator):
        assert clockify_report_generator.format_duration(None) is None
        assert clockify_report_generator.format_duration("PT2H30M") == "2H 30M"
        assert clockify_report_generator.format_duration("PT1M30S") == "1M 30S"
        assert clockify_report_generator.format_duration("PT3H45S") == "3H 45S"
        assert clockify_report_generator.format_duration("PT2H") == "2H"
        assert clockify_report_generator.format_duration("PT45M") == "45M"
        assert clockify_report_generator.format_duration("PT30S") == "30S"

    @mock.patch('ClockifyAPI.requests.get')
    def test_send_get_request(self, mock_get_request, clockify_api):
        mock_response = MagicMock()
        expected_response = {'id': '123', 'description': 'Test Result'}
        mock_response.json.return_value = expected_response
        mock_get_request.return_value = mock_response

        endpoint = 'test-endpoint'
        params = {'key': 'value'}
        result = clockify_api.send_get_request(endpoint, params=params)

        mock_get_request.assert_called_with(clockify_api.BASE_URL + endpoint, headers=mock.ANY, params=params)

        assert result == expected_response

    @mock.patch('ClockifyAPI.requests.get')
    def test_generate_raport_iteration_count(self, mock_get_request, clockify_report_generator):
        mock_responses = [
            [{'data': 'response1'}, {'data': 'response2'}, {'data': 'response3'}],
            [{'data': 'response4'}, {'data': 'response5'}],
            [],
        ]

        mock_get_request.return_value = MagicMock()
        mock_get_request.return_value.side_effect = mock_responses

        clockify_report_generator.generate_report('2023-05-15', '2023-05-16')

        assert mock_get_request.call_count == 4
