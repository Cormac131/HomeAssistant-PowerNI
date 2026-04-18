# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install test dependencies
python -m pip install -r requirements-test.txt

# Run unit tests (no network, no homeassistant required)
python -m pytest tests/test_parser.py -v

# Run live scrape tests (hits powerni.co.uk)
python -m pytest tests/test_live.py -v

# Skip live tests
POWER_NI_SKIP_LIVE=1 python -m pytest tests/ -v

# Run a single test
python -m pytest tests/test_parser.py::TestEVNightshift::test_night_rate_parsed -v
```

## Architecture

This is a Home Assistant HACS custom integration. HA loads `custom_components/power_ni/` as a package; the entry point is `__init__.py` → `coordinator.py` → `parser.py`.

**Separation of concerns:**
- `parser.py` — pure Python, no HA imports. All scraping logic lives here. Imported standalone by tests (via `conftest.py` `sys.path` manipulation) to avoid needing `homeassistant` installed.
- `coordinator.py` — wraps `parser.py` in a `DataUpdateCoordinator`, handles `aiohttp` fetch, runs `parse_page` in the executor.
- `sensor.py` — creates one `CoordinatorEntity` sensor per tariff/rate combination, driven entirely by `coordinator.data`.
- `const.py` — single source of truth for tariff definitions (`TARIFFS` dict keyed by section ID), rate keys, labels, and units.

**Scraping approach:** The page (`https://powerni.co.uk/compare-electricity-ni/unit-rates/`) is server-side rendered. Each tariff lives in a `<div id="<section-id>">` container. There are two table types:
- **Simple tables** (`tbl-rates` without `tbl-rates--multiline`): one unit rate per row. Best deal row has class `green-outline` or `pink-outline`. The incl. VAT price is the last `<td class="center">`.
- **Multiline tables** (`tbl-rates--multiline`): multiple rates per payment method (day/night/standing). The best deal `<tbody>` has class `pink-outline`. Each row has a `<span>` naming the time band; `_TIME_BAND_MAP` maps these to rate keys.

All prices scraped are **Best Deal incl. VAT**.

**Adding a new tariff:** Add an entry to `TARIFFS` in `const.py` with the `section_id` matching the `id` attribute on the page, `name`, and `rates` list. No other files need changing.

**Tests:** `tests/conftest.py` adds `custom_components/power_ni/` directly to `sys.path` so `parser` and `const` are importable as top-level modules without triggering `__init__.py`. The fixture in `tests/fixtures.py` mirrors the real page's HTML structure — keep it in sync if the page structure changes.

**CI:** `.github/workflows/scrape_check.yml` runs daily at 08:00 UTC. On schedule failures it auto-opens a GitHub issue (with deduplication). Live tests are skipped on PRs (`POWER_NI_SKIP_LIVE=1`).
