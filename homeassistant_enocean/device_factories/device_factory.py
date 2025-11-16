from abc import ABC, abstractmethod

from homeassistant_enocean.types import EnOceanSendRadioPacket
from ..device_type import EnOceanDeviceType
from ..address import EnOceanAddress, EnOceanDeviceAddress
from ..devices.device import EnOceanDevice

class EnOceanDeviceFactory(ABC):
    """Factory class to create EnOcean device handlers based on EEP."""

    @abstractmethod
    def create_device(self, enocean_id: EnOceanDeviceAddress, device_type: EnOceanDeviceType, send_packet: EnOceanSendRadioPacket | None = None, device_name: str | None = None, sender_id: EnOceanAddress=None) -> EnOceanDevice:
        """Create an EnOcean device based on the provided EEP."""
        pass
    

   