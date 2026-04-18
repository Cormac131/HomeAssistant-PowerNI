"""Pure parsing logic — no Home Assistant imports, so this is unit-testable standalone."""
from __future__ import annotations

import logging
import re

from bs4 import BeautifulSoup

try:
    from .const import TARIFFS  # when loaded as part of the HA package
except ImportError:
    from const import TARIFFS   # when loaded standalone for tests

_LOGGER = logging.getLogger(__name__)

# Maps the time-band span text on the page to our internal rate key.
_TIME_BAND_MAP: dict[str, str] = {
    "day rate": "day_rate",
    "day": "day_rate",
    "night rate": "night_rate",
    "night": "night_rate",
    "standing charge": "standing_charge",
}

_PRICE_RE = re.compile(r"^(\d+\.\d+)p\*?$")


def _parse_price(text: str) -> float | None:
    """Extract a float from a price cell like '30.22p*'."""
    m = _PRICE_RE.match(text.strip())
    if m:
        return float(m.group(1))
    return None


def _parse_simple_table(table) -> float | None:
    """Best-deal unit rate from a plain (non-multiline) rates table.

    The best deal row carries class 'green-outline' or 'pink-outline'.
    Falls back to the first tbody row if neither is present.
    The incl. VAT price is the last <td class="center"> in the row.
    """
    best_row = table.find("tr", class_=re.compile(r"(green|pink)-outline"))
    if best_row is None:
        tbody = table.find("tbody")
        best_row = tbody.find("tr") if tbody else None
    if best_row is None:
        return None

    center_tds = best_row.find_all("td", class_="center")
    if not center_tds:
        return None
    return _parse_price(center_tds[-1].get_text(strip=True))


def _parse_multiline_table(table) -> dict[str, float | None]:
    """Best-deal rates from a multi-rate table (EV / Economy 7).

    The best-deal tbody carries class 'pink-outline'.
    Each row has a <span> naming the time band and a last <td.center> with
    the incl. VAT price.
    """
    best_tbody = table.find("tbody", class_="pink-outline")
    if best_tbody is None:
        best_tbody = table.find("tbody")
    if best_tbody is None:
        return {}

    found: dict[str, float | None] = {}
    for row in best_tbody.find_all("tr"):
        # Skip the lbl-best label span; find the time-band span
        band_span = next(
            (s for s in row.find_all("span") if "lbl-best" not in (s.get("class") or [])),
            None,
        )
        if band_span is None:
            continue
        band = band_span.get_text(strip=True).lower()
        rate_key = _TIME_BAND_MAP.get(band)
        if rate_key is None:
            continue
        center_tds = row.find_all("td", class_="center")
        if center_tds:
            found[rate_key] = _parse_price(center_tds[-1].get_text(strip=True))

    return found


def parse_page(html: str) -> dict[str, dict[str, float | None]]:
    """Parse the Power NI unit rates page into structured price data."""
    soup = BeautifulSoup(html, "html.parser")
    data: dict[str, dict[str, float | None]] = {}

    for tariff_key, cfg in TARIFFS.items():
        section_id = cfg["section_id"]
        expected_rates = cfg["rates"]

        section = soup.find(id=section_id)
        if section is None:
            _LOGGER.warning("Section '%s' not found on page", section_id)
            data[tariff_key] = {r: None for r in expected_rates}
            continue

        table = section.find_next("table", class_="tbl-rates")
        if table is None:
            _LOGGER.warning("No rates table found for section '%s'", section_id)
            data[tariff_key] = {r: None for r in expected_rates}
            continue

        is_multiline = "tbl-rates--multiline" in (table.get("class") or [])

        if is_multiline:
            found = _parse_multiline_table(table)
        else:
            unit = _parse_simple_table(table)
            found = {"unit_rate": unit}

        data[tariff_key] = {r: found.get(r) for r in expected_rates}
        _LOGGER.debug("Parsed %s: %s", tariff_key, data[tariff_key])

    return data
