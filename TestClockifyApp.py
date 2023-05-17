import pytest
from main import ClockifyApp

class TestClockifyApp:

    @pytest.fixture
    def clockify(self):
        return ClockifyApp()

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
        assert clockify.validate_date_format("1212-05-03", "4444-05-2023") is False
        assert clockify.validate_date_format("23-12-01", "23-12-31") is False

    def test_validate_date_format_invalid_month(self, clockify):
        assert clockify.validate_date_format("2023-15-14", "2023-12-03") is False
        assert clockify.validate_date_format("2023-00-10", "2023-05-23") is False
        assert clockify.validate_date_format("2023-30-03", "2023-05-2023") is False

    def test_validate_date_format_invalid_day(self, clockify):
        assert clockify.validate_date_format("2023-02-29", "2023-12-03") is False
        assert clockify.validate_date_format("2023-05-00", "2023-05-23") is False
        assert clockify.validate_date_format("2023-05-32", "2023-05-2023") is False
