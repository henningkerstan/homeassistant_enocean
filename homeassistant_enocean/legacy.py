"""Legacy imports from the underlying 'enocean' library for backward compatibility.

This module re-exports selected classes and functions from the 'enocean' library
to maintain compatibility with existing code that relies on these imports.

It will be removed in future versions, as soon as the Home Assistant integration
code has been migrated to use the 'homeassistant_enocean' library instead.
"""

from enocean.communicators import SerialCommunicator
from enocean.protocol.packet import Packet, RadioPacket
from enocean.utils import combine_hex

from homeassistant_enocean.device_type import EnOceanDeviceType

from .eep import EEP

BINARY_SENSOR_DEVICE_TYPE = (
    EnOceanDeviceType(
        eep=EEP(0xF6, 0x02, 0x01),
        model="Light and Blind Control - Application Style 2",
    ),
)

__all__ = [
    "combine_hex",
    "SerialCommunicator",
    "Packet",
    "RadioPacket",
]


# need to supply a list of entries per device id (b/c multiple instances are allowed in old configuration.yaml)
class EnOceanDeviceConfigYAML:
    """Configuration for an EnOcean device from legacy configuration.yaml."""

    def __init__(
        self,
        platform: str,
        device_class: str,
        name: str,
        channel: int,
        range_from: int,
        range_to: int,
    ) -> None:
        """Initialize the EnOcean device configuration."""
        self.platform = platform
        self.device_class = device_class
        self.name = name
        self.channel = channel
        self.range_from = range_from
        self.range_to = range_to


def infer_eep_from_configurations_for_device(
    configs: list[EnOceanDeviceConfigYAML],
) -> EEP | None:
    """infer the EEP based on the legacy configuration."""

    if configs is None or len(configs) == 0:
        return None

    # For simplicity, we first only consider the first configuration entry
    config = configs[0]

    if config.platform == "binary_sensor":
        # ignore any other entries for now
        return EEP(0xF6, 0x02, 0x01)

    if config.platform == "light":
        # ignore any other entries for now
        return EEP(0xA5, 0x08, 0x01)

    if config.platform == "switch":
        # determine number of channels from all entries
        max_channel = 0
        for c in configs:
            if c.platform != "switch":
                continue

            if c.channel > max_channel:
                max_channel = c.channel

        if max_channel == 0:
            return EEP(0xD2, 0x01, 0x0F)
        elif max_channel == 1:
            return EEP(0xD2, 0x01, 0x10)
        elif max_channel <= 3:
            return EEP(0xD2, 0x01, 0x13)
        elif max_channel <= 7:
            return EEP(0xD2, 0x01, 0x14)

        return None

    if config.platform == "sensor":
        if config.device_class == "windowhandle":
            # Window handle does not have additional sensors, so return that
            return EEP(0xF6, 0x10, 0x00)

        if config.device_class == "powersensor":
            return EEP(0xA5, 0x12, 0x01)
