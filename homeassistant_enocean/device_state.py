"""Representation of an EnOcean device state."""
from .address import EnOceanDeviceAddress, EnOceanAddress


class EnOceanDeviceState:
    """Representation of an EnOcean device."""
    enocean_id: EnOceanDeviceAddress | None = None
    sender_id: EnOceanAddress | None = None
    