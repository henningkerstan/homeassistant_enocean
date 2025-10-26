"""Representation of an EnOcean device state."""
from .cover_state import EnOceanCoverState
from .device_type import EnOceanDeviceType
from .entity_name import EntityName
from .id import EnOceanID
from .light_state import EnOceanLightState


class EnOceanDeviceProperties:
    """Representation of an EnOcean device."""

    binary_sensor_is_on: dict[EntityName, bool] = {}
    switch_is_on: dict[EntityName, bool] = {}
    cover_state: dict[EntityName, EnOceanCoverState] = {}
    light_state: dict[EntityName, EnOceanLightState] = {}

    device_name: str | None = None
    
    def __init__(self, enocean_id: EnOceanID, device_type: EnOceanDeviceType):
        """Construct an EnOcean device."""
        self.__enocean_id = enocean_id
        self.__device_type = device_type

    @property
    def enocean_id(self) -> EnOceanID:
        """Return the device ID."""
        return self.__enocean_id

    @property
    def device_type(self) -> EnOceanDeviceType:
        """Return the device type."""
        return self.__device_type