from abc import ABC, abstractmethod
from typing import Callable

from homeassistant_enocean.address import EnOceanAddress
from homeassistant_enocean.entity_properties import EnOceanEntityProperties
from homeassistant_enocean.cover_properties import EnOceanCoverProperties
from homeassistant_enocean.device_state import EnOceanDeviceState
from enocean.protocol.packet import RadioPacket
from homeassistant_enocean.entity_id import EnOceanEntityID


class EEPHandler(ABC):
    """Abstract base class for EnOcean Equipment Profile (EEP) handlers."""

    def __init__(self, send_packet: Callable[[RadioPacket], None] | None = None) -> None:
        """Construct EEP handler."""
        self.__send_packet = send_packet


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


    def binary_sensor_entities(self) -> list[EnOceanEntityProperties]:
        """Return the list of binary sensor entities handled by this EEP handler."""
        return []

    def cover_entities(self) -> list[EnOceanCoverProperties]:
        """Return the list of cover entities handled by this EEP handler."""
        return []