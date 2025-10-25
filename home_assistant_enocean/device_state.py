from home_assistant_enocean.binary_sensor import BinarySensor
from home_assistant_enocean.cover_state import Cover, EnOceanCoverState
from home_assistant_enocean.device_type import DeviceType
from home_assistant_enocean.entity_name import EntityName
from home_assistant_enocean.enocean_id import EnOceanID
from home_assistant_enocean.switch import Switch


class EnOceanDeviceState:
    """Representation of an EnOcean device."""

    binary_sensor_is_on: dict[EntityName, bool] = {}
    switch_is_on: dict[EntityName, bool] = {}
    cover_state: dict[EntityName, EnOceanCoverState] = {}
    sensors: dict[EntityName, object] = {}
    events: dict[EntityName, object] = {}
    
    def __init__(self, enocean_id: EnOceanID, device_type: DeviceType):
        """Construct an EnOcean device."""
        self.__enocean_id = enocean_id
        self.__device_type = device_type

    @property
    def enocean_id(self) -> EnOceanID:
        """Return the device ID."""
        return self.__enocean_id

    @property
    def device_type(self) -> DeviceType:
        """Return the device type."""
        return self.__device_type