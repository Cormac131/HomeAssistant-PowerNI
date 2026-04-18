"""Live scrape test — hits powerni.co.uk and verifies all tariff prices are found.

Run with: pytest tests/test_live.py -v
Skipped automatically if POWER_NI_SKIP_LIVE=1 is set.
"""
import os
import pytest
import aiohttp
import asyncio

import parser as power_ni_parser  # via conftest.py sys.path
import const as power_ni_const    # via conftest.py sys.path

SKIP_LIVE = os.getenv("POWER_NI_SKIP_LIVE", "0") == "1"


async def _fetch_and_parse() -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            power_ni_const.SCRAPE_URL,
            timeout=aiohttp.ClientTimeout(total=30),
        ) as resp:
            resp.raise_for_status()
            html = await resp.text()
    return power_ni_parser.parse_page(html)


@pytest.fixture(scope="module")
def live_data():
    return asyncio.run(_fetch_and_parse())


@pytest.mark.skipif(SKIP_LIVE, reason="POWER_NI_SKIP_LIVE is set")
class TestLiveScrape:
    """Fail loudly if the website has changed and prices can no longer be scraped."""

    @pytest.mark.parametrize("tariff_key,rate_key", [
        ("eco_energy", "unit_rate"),
        ("bill_pay", "unit_rate"),
        ("keypad", "unit_rate"),
        ("ev_anytime", "day_rate"),
        ("ev_anytime", "standing_charge"),
        ("ev_nightshift", "night_rate"),
        ("ev_nightshift", "day_rate"),
        ("ev_nightshift", "standing_charge"),
        ("bill_pay_economy_7", "day_rate"),
        ("bill_pay_economy_7", "night_rate"),
        ("bill_pay_economy_7", "standing_charge"),
        ("keypad_economy_7", "day_rate"),
        ("keypad_economy_7", "night_rate"),
        ("keypad_economy_7", "standing_charge"),
    ])
    def test_rate_is_scraped(self, live_data, tariff_key, rate_key):
        value = live_data.get(tariff_key, {}).get(rate_key)
        assert value is not None, (
            f"SCRAPE FAILURE: {tariff_key}.{rate_key} returned None.\n"
            f"The Power NI website structure may have changed at {power_ni_const.SCRAPE_URL}.\n"
            "Check parser.py selectors."
        )
        assert isinstance(value, float), f"{tariff_key}.{rate_key} should be a float, got {type(value)}"
        assert value > 0, f"{tariff_key}.{rate_key} = {value} is not a positive number"

    def test_unit_rates_are_plausible(self, live_data):
        """kWh prices should be between 1p and 100p."""
        kwh_keys = [
            ("eco_energy", "unit_rate"),
            ("bill_pay", "unit_rate"),
            ("keypad", "unit_rate"),
            ("ev_anytime", "day_rate"),
            ("ev_nightshift", "day_rate"),
            ("ev_nightshift", "night_rate"),
            ("bill_pay_economy_7", "day_rate"),
            ("bill_pay_economy_7", "night_rate"),
            ("keypad_economy_7", "day_rate"),
            ("keypad_economy_7", "night_rate"),
        ]
        for tariff_key, rate_key in kwh_keys:
            value = live_data.get(tariff_key, {}).get(rate_key)
            if value is not None:
                assert 1.0 <= value <= 100.0, (
                    f"{tariff_key}.{rate_key} = {value}p/kWh is outside plausible range 1–100p"
                )

    def test_standing_charges_are_plausible(self, live_data):
        """Standing charges should be between 1p and 100p/day."""
        for tariff_key, rate_key in [
            ("ev_anytime", "standing_charge"),
            ("ev_nightshift", "standing_charge"),
            ("bill_pay_economy_7", "standing_charge"),
            ("keypad_economy_7", "standing_charge"),
        ]:
            value = live_data.get(tariff_key, {}).get(rate_key)
            if value is not None:
                assert 1.0 <= value <= 100.0, (
                    f"{tariff_key}.{rate_key} = {value}p/day is outside plausible range 1–100p"
                )
