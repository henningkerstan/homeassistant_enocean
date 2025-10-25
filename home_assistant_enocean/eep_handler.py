from abc import ABC, abstractmethod

from home_assistant_enocean.device import EnOceanDeviceState
from enocean.protocol.packet import RadioPacket
from home_assistant_enocean.entity import EnOceanEntity


class EEPHandler(ABC):
    """Abstract base class for EnOcean Equipment Profile (EEP) handlers."""
    def handle_packet(self, packet: RadioPacket, device_state: EnOceanDeviceState) -> list[EnOceanEntity]:
        """Handle an incoming EnOcean packet and return the entities affected."""
        if packet.sender_int == device_state.enocean_id.to_number():
            self.__handle_packet(packet, device_state)


    @abstractmethod
    def __handle_packet(self, packet: RadioPacket, device_state: EnOceanDeviceState) -> list[EnOceanEntity]:
        """Handle an incoming EnOcean packet."""
        pass