from abc import ABC, abstractmethod
from typing import Callable

from homeassistant_enocean.address import EnOceanAddress, EnOceanDeviceAddress
from homeassistant_enocean.entity_properties import HomeAssistantEntityProperties
from homeassistant_enocean.device_state import EnOceanDeviceState
from enocean.protocol.packet import RadioPacket
from homeassistant_enocean.entity_id import EnOceanEntityID
from homeassistant_enocean.types import EnOceanBinarySensorCallback, EnOceanCoverCallback, EnOceanEntityUID, EnOceanLightCallback, EnOceanSwitchCallback




class EEPHandler(ABC):
    """Abstract base class for EnOcean Equipment Profile (EEP) handlers."""

    def __init__(self, send_packet: Callable[[RadioPacket], None] | None = None, enocean_id: EnOceanDeviceAddress | None = None, sender_id: EnOceanAddress | None = None) -> None:
        """Construct EEP handler."""
        self.__send_packet = send_packet

        # callbacks
        self._binary_sensor_callbacks: dict[EnOceanEntityUID, EnOceanBinarySensorCallback] = {}
        self._cover_callbacks: dict[EnOceanEntityUID, EnOceanCoverCallback] = {}
        self._light_callbacks: dict[EnOceanEntityUID, EnOceanLightCallback] = {}
        self._switch_callbacks: dict[EnOceanEntityUID, EnOceanSwitchCallback] = {}

        # entities
        self._binary_sensor_entities: list[HomeAssistantEntityProperties] = []
        self._cover_entities: list[HomeAssistantEntityProperties] = []
        self._light_entities: list[HomeAssistantEntityProperties] = []
        self._switch_entities: list[HomeAssistantEntityProperties] = []
        self.initialize_entities()


    @property
    def send_packet(self) -> Callable[[RadioPacket], None] | None:
        """Return the send packet function."""
        return self.__send_packet


    def handle_packet(self, packet: RadioPacket, enocean_id: EnOceanDeviceAddress, sender_id: EnOceanAddress) -> None:
        """Handle an incoming EnOcean packet."""
        print(f"EEPHandler.handle_packet: Checking packet from sender {EnOceanAddress.from_number(packet.sender_int)} against device ID {enocean_id.to_string()}")
        if packet.sender_int == enocean_id.to_number():
            self.handle_matching_packet(packet, enocean_id, sender_id)

    @abstractmethod
    def initialize_entities(self) -> None:
        """Initialize the entities handled by this EEP handler."""
        pass

    @abstractmethod
    def handle_matching_packet(self, packet: RadioPacket, enocean_id: EnOceanDeviceAddress, sender_id: EnOceanAddress) -> None:
        """Handle an incoming EnOcean packet."""
        pass

    # binary sensors
    @property    
    def binary_sensor_entities(self) -> list[HomeAssistantEntityProperties]:
        """Return the list of binary sensor entities handled by this EEP handler."""
        return self._binary_sensor_entities
    
    @property
    def cover_entities(self) -> list[HomeAssistantEntityProperties]:
        """Return the list of cover entities handled by this EEP handler."""
        return self._cover_entities
    
    @property
    def light_entities(self) -> list[HomeAssistantEntityProperties]:
        """Return the list of light entities handled by this EEP handler."""
        return self._light_entities
    
    @property
    def switch_entities(self) -> list[HomeAssistantEntityProperties]:
        """Return the list of switch entities handled by this EEP handler."""
        return self._switch_entities
    

    def binary_sensor_attach_callback(self, unique_id: str, callback: EnOceanBinarySensorCallback) -> None:
        """Attach a callback for binary sensor state changes."""
        self._binary_sensor_callbacks[unique_id] = callback


    
    

    def cover_attach_callback(self, unique_id: str, callback: EnOceanCoverCallback) -> None:
        """Attach a callback for cover state changes."""
        self._cover_callbacks[unique_id] = callback