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


class TestRobustness:
    """Verify the parser never raises — it always returns a complete dict with float-or-None
    values regardless of what the page contains. HA marks sensors unavailable when
    native_value is None, so None is always safe; an exception is not."""

    def test_empty_string_does_not_raise(self):
        data = power_ni_parser.parse_page("")
        assert isinstance(data, dict)

    def test_malformed_html_does_not_raise(self):
        data = power_ni_parser.parse_page("<html><div><p><<broken>>")
        assert isinstance(data, dict)

    def test_truncated_html_does_not_raise(self):
        from tests.fixtures import MOCK_HTML
        data = power_ni_parser.parse_page(MOCK_HTML[:200])
        assert isinstance(data, dict)

    def test_section_present_but_no_table(self):
        html = '<html><body><div id="bill-pay"><h3>Bill Pay</h3><p>no table here</p></div></body></html>'
        data = power_ni_parser.parse_page(html)
        assert isinstance(data, dict)
        for value in data["bill_pay"].values():
            assert value is None

    def test_garbled_price_text_returns_none_not_exception(self):
        html = """<html><body>
        <div id="bill-pay"><h3>Bill Pay</h3>
        <table class="tbl-rates unit-rates"><tbody>
          <tr class="pink-outline">
            <td>Best Deal</td><td>-</td>
            <td class="center">TBC</td><td class="center">TBC</td>
          </tr>
        </tbody></table></div></body></html>"""
        data = power_ni_parser.parse_page(html)
        assert isinstance(data, dict)
        assert data["bill_pay"]["unit_rate"] is None

    def test_return_value_always_contains_all_tariff_keys(self):
        data = power_ni_parser.parse_page("")
        import const as power_ni_const
        assert set(data.keys()) == set(power_ni_const.TARIFFS.keys())

    def test_return_value_always_contains_all_rate_keys(self):
        data = power_ni_parser.parse_page("")
        import const as power_ni_const
        for tariff_key, cfg in power_ni_const.TARIFFS.items():
            assert set(data[tariff_key].keys()) == set(cfg["rates"])

    def test_all_values_are_float_or_none(self):
        from tests.fixtures import MOCK_HTML
        data = power_ni_parser.parse_page(MOCK_HTML)
        for tariff_key, rates in data.items():
            for rate_key, value in rates.items():
                assert value is None or isinstance(value, float), (
                    f"{tariff_key}.{rate_key} = {value!r} is neither float nor None"
                )


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
