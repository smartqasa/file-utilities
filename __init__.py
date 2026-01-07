from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .custom_components.file_utilities.const import DOMAIN
from .custom_components.file_utilities.services import register_file_services


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the File Utilities integration."""

    hass.data.setdefault(DOMAIN, {})

    register_file_services(hass)

    return True
