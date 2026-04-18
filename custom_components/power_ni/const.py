DOMAIN = "power_ni"
SCRAPE_URL = "https://powerni.co.uk/compare-electricity-ni/unit-rates/"
DEFAULT_SCAN_INTERVAL = 3600  # 1 hour

# Each tariff maps to a section ID on the page and the rates it exposes.
# All prices are the "Best Deal" incl. VAT rate for that tariff section.
TARIFFS = {
    "eco_energy": {
        "name": "Eco Energy",
        "section_id": "eco-energy",
        "rates": ["unit_rate"],
    },
    "bill_pay": {
        "name": "Bill Pay",
        "section_id": "bill-pay",
        "rates": ["unit_rate"],
    },
    "keypad": {
        "name": "Keypad",
        "section_id": "keypad",
        "rates": ["unit_rate"],
    },
    "ev_anytime": {
        "name": "Electric Vehicle Anytime",
        "section_id": "electric-vehicle-anytime",
        "rates": ["day_rate", "standing_charge"],
    },
    "ev_nightshift": {
        "name": "Electric Vehicle Nightshift",
        "section_id": "electric-vehicle-nightshift",
        "rates": ["night_rate", "day_rate", "standing_charge"],
    },
    "bill_pay_economy_7": {
        "name": "Bill Pay Economy 7",
        "section_id": "bill-pay-economy-7",
        "rates": ["day_rate", "night_rate", "standing_charge"],
    },
    "keypad_economy_7": {
        "name": "Keypad Economy 7",
        "section_id": "keypad-economy-7",
        "rates": ["day_rate", "night_rate", "standing_charge"],
    },
}

RATE_LABELS = {
    "unit_rate": "Unit Rate",
    "day_rate": "Day Rate",
    "night_rate": "Night Rate",
    "standing_charge": "Standing Charge",
}

RATE_UNITS = {
    "unit_rate": "p/kWh",
    "day_rate": "p/kWh",
    "night_rate": "p/kWh",
    "standing_charge": "p/day",
}
