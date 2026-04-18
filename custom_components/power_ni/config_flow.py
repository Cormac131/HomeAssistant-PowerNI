"""Config flow for Power NI integration."""
from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries

from .const import DOMAIN


class PowerNIConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the initial setup via UI."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            return self.async_create_entry(title="Power NI", data={})

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({}),
            description_placeholders={"url": "https://powerni.co.uk/compare-electricity-ni/unit-rates/"},
        )
