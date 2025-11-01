"""Representation of an EnOcean device state."""
from .cover_state import EnOceanCoverState
from .device_type import EnOceanDeviceType
from .types import EnOceanEntityUID
from .address import EnOceanAddress
from .light_state import EnOceanLightState


class EnOceanDeviceState:
    """Representation of an EnOcean device."""

    binary_sensor_is_on: dict[EnOceanEntityUID, bool] = {}
    switch_is_on: dict[EnOceanEntityUID, bool] = {}
    cover_state: dict[EnOceanEntityUID, EnOceanCoverState] = {}
    light_state: dict[EnOceanEntityUID, EnOceanLightState] = {}


    device_name: str | None = None

    def __init__(self, enocean_id: EnOceanAddress, device_type: EnOceanDeviceType, device_name: str | None = None, sender_id: EnOceanAddress | None = None) -> None:
        """Construct an EnOcean device."""
        self.__enocean_id = enocean_id
        self.__device_type = device_type
        self.device_name = device_name
        self.__sender_id = sender_id

    @property
    def enocean_id(self) -> EnOceanAddress:
        """Return the device ID."""
        return self.__enocean_id

    @property
    def device_type(self) -> EnOceanDeviceType:
        """Return the device type."""
        return self.__device_type
    

    @property
    def sender_id(self) -> EnOceanAddress | None:
        """Return the sender ID."""
        return self.__sender_id