from abc import ABC, abstractmethod
from typing import Callable

from homeassistant_enocean.address import EnOceanAddress
from homeassistant_enocean.entity_properties import HomeAssistantEntityProperties
from homeassistant_enocean.device_state import EnOceanDeviceState
from enocean.protocol.packet import RadioPacket
from homeassistant_enocean.entity_id import EnOceanEntityID
from homeassistant_enocean.types import EnOceanBinarySensorCallback, EnOceanCoverCallback, EnOceanEntityUID, EnOceanLightCallback, EnOceanSwitchCallback




class EEPHandler(ABC):
    """Abstract base class for EnOcean Equipment Profile (EEP) handlers."""

    def __init__(self, send_packet: Callable[[RadioPacket], None] | None = None) -> None:
        """Construct EEP handler."""
        self.__send_packet = send_packet
        self.__binary_sensor_callbacks: dict[EnOceanEntityUID, EnOceanBinarySensorCallback] = {}
        self.__cover_callbacks: dict[EnOceanEntityUID, EnOceanCoverCallback] = {}
        self.__light_callbacks: dict[EnOceanEntityUID, EnOceanLightCallback] = {}
        self.__switch_callbacks: dict[EnOceanEntityUID, EnOceanSwitchCallback] = {}


    def initialize_device_state(self, state: EnOceanDeviceState) -> None:
        """Initialize the device state for this EEP handler."""
        pass

    @property
    def send_packet(self) -> Callable[[RadioPacket], None] | None:
        """Return the send packet function."""
        return self.__send_packet


    def handle_packet(self, packet: RadioPacket, device_state: EnOceanDeviceState) -> list[EnOceanEntityID]:
        """Handle an incoming EnOcean packet and return the entities affected."""
        print(f"EEPHandler.handle_packet: Checking packet from sender {EnOceanAddress.from_number(packet.sender_int)} against device ID {device_state.enocean_id.to_string()}")
        if packet.sender_int == device_state.enocean_id.to_number():
            return self.handle_packet_matching(packet, device_state)
        
        return []


    @abstractmethod
    def handle_packet_matching(self, packet: RadioPacket, device_state: EnOceanDeviceState) -> list[EnOceanEntityID]:
        """Handle an incoming EnOcean packet."""
        pass

    # binary sensors
    def binary_sensor_entities(self) -> list[HomeAssistantEntityProperties]:
        """Return the list of binary sensor entities handled by this EEP handler."""
        return []

    def binary_sensor_attach_callback(self, unique_id: str, callback: EnOceanBinarySensorCallback) -> None:
        """Attach a callback for binary sensor state changes."""
        self.__binary_sensor_callbacks[unique_id] = callback


    # covers
    def cover_entities(self) -> list[HomeAssistantEntityProperties]:
        """Return the list of cover entities handled by this EEP handler."""
        return []
    

    def cover_attach_callback(self, unique_id: str, callback: EnOceanCoverCallback) -> None:
        """Attach a callback for cover state changes."""
        self.__cover_callbacks[unique_id] = callback