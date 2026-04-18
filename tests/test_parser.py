"""Unit tests for the Power NI HTML parser using a local fixture."""
import pytest
import parser as power_ni_parser  # custom_components/power_ni/parser.py via conftest.py
from tests.fixtures import MOCK_HTML


@pytest.fixture
def parsed():
    return power_ni_parser.parse_page(MOCK_HTML)


class TestEcoEnergy:
    def test_unit_rate_parsed(self, parsed):
        assert parsed["eco_energy"]["unit_rate"] == 30.22


class TestBillPay:
    def test_unit_rate_parsed(self, parsed):
        assert parsed["bill_pay"]["unit_rate"] == 30.22


class TestKeypad:
    def test_unit_rate_parsed(self, parsed):
        assert parsed["keypad"]["unit_rate"] == 30.53


class TestEVAnytime:
    def test_day_rate_parsed(self, parsed):
        assert parsed["ev_anytime"]["day_rate"] == 28.84

    def test_standing_charge_parsed(self, parsed):
        assert parsed["ev_anytime"]["standing_charge"] == 12.10


class TestEVNightshift:
    def test_night_rate_parsed(self, parsed):
        assert parsed["ev_nightshift"]["night_rate"] == 16.80

    def test_day_rate_parsed(self, parsed):
        assert parsed["ev_nightshift"]["day_rate"] == 35.14

    def test_standing_charge_parsed(self, parsed):
        assert parsed["ev_nightshift"]["standing_charge"] == 12.10


class TestBillPayEconomy7:
    def test_day_rate_parsed(self, parsed):
        assert parsed["bill_pay_economy_7"]["day_rate"] == 35.17

    def test_night_rate_parsed(self, parsed):
        assert parsed["bill_pay_economy_7"]["night_rate"] == 16.81

    def test_standing_charge_parsed(self, parsed):
        assert parsed["bill_pay_economy_7"]["standing_charge"] == 12.10


class TestKeypadEconomy7:
    def test_day_rate_parsed(self, parsed):
        assert parsed["keypad_economy_7"]["day_rate"] == 36.50

    def test_night_rate_parsed(self, parsed):
        assert parsed["keypad_economy_7"]["night_rate"] == 17.45

    def test_standing_charge_parsed(self, parsed):
        assert parsed["keypad_economy_7"]["standing_charge"] == 12.55


class TestMissingSection:
    def test_missing_section_returns_none_values(self):
        data = power_ni_parser.parse_page("<html><body>No tariffs here</body></html>")
        for tariff_key, values in data.items():
            for rate_key, value in values.items():
                assert value is None, f"{tariff_key}.{rate_key} should be None for empty page"


class TestPriceValidity:
    def test_all_rates_are_positive(self, parsed):
        for tariff_key, rates in parsed.items():
            for rate_key, value in rates.items():
                if value is not None:
                    assert value > 0, f"{tariff_key}.{rate_key} must be positive, got {value}"

    def test_no_unexpected_none_values(self, parsed):
        for tariff_key, rates in parsed.items():
            for rate_key, value in rates.items():
                assert value is not None, (
                    f"{tariff_key}.{rate_key} was None — "
                    "parser failed to extract a price that should be present"
                )
