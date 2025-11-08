"""Representation of an EnOcean device state."""
from .cover_state import EnOceanCoverState
from .types import EnOceanEntityUID
from .light_state import EnOceanLightState
from .address import EnOceanDeviceAddress, EnOceanAddress


class EnOceanDeviceState:
    """Representation of an EnOcean device."""

    binary_sensor_is_on: dict[EnOceanEntityUID, bool] = {}
    switch_is_on: dict[EnOceanEntityUID, bool] = {}
    cover_state: dict[EnOceanEntityUID, EnOceanCoverState] = {}
    light_state: dict[EnOceanEntityUID, EnOceanLightState] = {}

    enocean_id: EnOceanDeviceAddress | None = None
    sender_id: EnOceanAddress | None = None
    