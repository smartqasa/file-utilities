import asyncio
import os
import tempfile
from typing import Any, cast

import voluptuous as vol

from homeassistant.core import HomeAssistant, ServiceCall, SupportsResponse
import homeassistant.helpers.config_validation as cv

from .const import (
    DOMAIN,
    ALLOWED_ROOTS,
    SERVICE_READ,
    SERVICE_WRITE,
    ATTR_PATH,
    ATTR_CONTENT,
    ATTR_ENCODING,
    ATTR_CREATE,
    ATTR_ATOMIC,
)
from .path import validate_path, PathValidationError

ServiceResponse = dict[str, Any]

# Single integration-wide lock
_FILE_LOCK = asyncio.Lock()


def register_file_services(hass: HomeAssistant) -> None:
    """Register file utility services."""

    async def handle_read(call: ServiceCall) -> ServiceResponse:
        try:
            path = validate_path(call.data[ATTR_PATH], ALLOWED_ROOTS)
        except PathValidationError as err:
            raise ValueError(str(err))

        encoding: str = call.data.get(ATTR_ENCODING, "utf-8")

        async with _FILE_LOCK:
            try:
                with open(path, "r", encoding=encoding) as f:
                    content = f.read()
            except FileNotFoundError:
                raise ValueError(f"File not found: {path}")

        return {"success": True,"content": content}

    async def handle_write(call: ServiceCall) -> ServiceResponse:
        try:
            path = validate_path(call.data[ATTR_PATH], ALLOWED_ROOTS)
        except PathValidationError as err:
            raise ValueError(str(err))

        content: str = call.data[ATTR_CONTENT]
        encoding: str = call.data.get(ATTR_ENCODING, "utf-8")
        create: bool = call.data.get(ATTR_CREATE, True)
        atomic: bool = call.data.get(ATTR_ATOMIC, True)

        async with _FILE_LOCK:
            if not create and not os.path.exists(path):
                raise ValueError(f"File does not exist: {path}")

            if atomic:
                directory = os.path.dirname(path)
                fd, tmp_path = tempfile.mkstemp(dir=directory)
                try:
                    with os.fdopen(fd, "w", encoding=encoding) as f:
                        f.write(content)
                        f.flush()
                        os.fsync(f.fileno())
                    os.replace(tmp_path, path)
                finally:
                    if os.path.exists(tmp_path):
                        os.unlink(tmp_path)
            else:
                with open(path, "w", encoding=encoding) as f:
                    f.write(content)
        return {
            "success": True,
            "path": path,
            "atomic": atomic,
        }

    # READ
    hass.services.async_register(
        DOMAIN,
        SERVICE_READ,
        handle_read,
        schema=vol.Schema(
            {
                vol.Required(ATTR_PATH): cv.string,
                vol.Optional(ATTR_ENCODING, default="utf-8"): cv.string,
            }
        ),
        supports_response=SupportsResponse.ONLY,
    )

    # WRITE
    hass.services.async_register(
        DOMAIN,
        SERVICE_WRITE,
        handle_write,
        schema=vol.Schema(
            {
                vol.Required(ATTR_PATH): cv.string,
                vol.Required(ATTR_CONTENT): cv.string,
                vol.Optional(ATTR_ENCODING, default="utf-8"): cv.string,
                vol.Optional(ATTR_CREATE, default=True): cv.boolean,
                vol.Optional(ATTR_ATOMIC, default=True): cv.boolean,
            }
        ),
        supports_response=SupportsResponse.ONLY,
    )
