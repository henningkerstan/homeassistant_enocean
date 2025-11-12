"""Representation of an EnOcean device state."""
from homeassistant_enocean.entity_properties import HomeAssistantEntityProperties
from homeassistant_enocean.device_state import EnOceanDeviceState
from homeassistant_enocean.eep_handlers.eep_handler import EEPHandler
from .device_type import EnOceanDeviceType
from .address import EnOceanAddress, EnOceanDeviceAddress


class EnOceanDevice:
    """Representation of an EnOcean device."""
    

    def __init__(self, enocean_id: EnOceanDeviceAddress, device_type: EnOceanDeviceType, handler: EEPHandler, device_name: str | None = None, sender_id: EnOceanAddress | None = None) -> None:
        """Construct an EnOcean device."""
        self.state: EnOceanDeviceState = EnOceanDeviceState()
        self.state.enocean_id = enocean_id
        self.__device_type = device_type
        self.__handler = handler
        self.device_name = device_name
        self.state.sender_id = sender_id

    @property
    def enocean_id(self) -> EnOceanDeviceAddress:
        """Return the device ID."""
        return self.state.enocean_id

    @property
    def device_type(self) -> EnOceanDeviceType:
        """Return the device type."""
        return self.__device_type

    @property
    def handler(self) -> EEPHandler: 
        """Return the EEP handler."""
        return self.__handler

    @property
    def sender_id(self) -> EnOceanAddress | None:
        """Return the sender ID."""
        return self.state.sender_id
    
    @sender_id.setter
    def sender_id(self, value: EnOceanAddress | None) -> None:
        """Set the sender ID."""
        self.state.sender_id = value

    @property
    def binary_sensor_entities(self) -> list[HomeAssistantEntityProperties]:
        """Return the binary sensor entities."""
        return self.__handler.binary_sensor_entities

    @property
    def cover_entities(self) -> list[HomeAssistantEntityProperties]:
        """Return the cover entities."""
        return self.__handler.cover_entities    
    
    @property
    def event_entities(self) -> list[HomeAssistantEntityProperties]:
        """Return the event entities."""
        return []

    @property
    def light_entities(self) -> list[HomeAssistantEntityProperties]:
        """Return the light entities."""
        return self.__handler.light_entities
    

    @property
    def sensor_entities(self) -> list[HomeAssistantEntityProperties]:
        """Return the sensor entities."""
        return self.__handler.sensor_entities

    @property
    def switch_entities(self) -> list[HomeAssistantEntityProperties]:
        """Return the switch entities."""
        return self.__handler.switch_entities

    