from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN
from .services import register_file_services


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the File Utilities integration."""

    hass.data.setdefault(DOMAIN, {})

    register_file_services(hass)

    return True
