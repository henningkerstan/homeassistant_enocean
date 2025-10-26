from abc import ABC, abstractmethod

from home_assistant_enocean.device_properties import EnOceanDeviceProperties
from enocean.protocol.packet import RadioPacket
from home_assistant_enocean.entity import EnOceanEntity


class EEPHandler(ABC):
    """Abstract base class for EnOcean Equipment Profile (EEP) handlers."""
    def handle_packet(self, packet: RadioPacket, device_state: EnOceanDeviceProperties) -> list[EnOceanEntity]:
        """Handle an incoming EnOcean packet and return the entities affected."""
        if packet.sender_int == device_state.enocean_id.to_number():
            return self.handle_packet_matching(packet, device_state)
        
        return []


    @abstractmethod
    def handle_packet_matching(self, packet: RadioPacket, device_state: EnOceanDeviceProperties) -> list[EnOceanEntity]:
        """Handle an incoming EnOcean packet."""
        pass


    def binary_sensor_entities(self) -> list[str]:
        """Return the list of binary sensor entities handled by this EEP handler."""
        return []