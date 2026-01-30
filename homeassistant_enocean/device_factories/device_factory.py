from abc import ABC, abstractmethod

from ..address import EnOceanAddress, EnOceanDeviceAddress
from ..device_type import EnOceanDeviceType
from ..devices.device import EnOceanDevice
from ..types import EnOceanSendRadioPacket, HomeAssistantTaskCreator


class EnOceanDeviceFactory(ABC):
    """Factory class to create EnOcean devices based on EEP."""

    @abstractmethod
    def create_device(
        self,
        enocean_id: EnOceanDeviceAddress,
        device_type: EnOceanDeviceType,
        send_packet: EnOceanSendRadioPacket | None = None,
        device_name: str | None = None,
        sender_id: EnOceanAddress = None,
        create_task: HomeAssistantTaskCreator | None = None,
    ) -> EnOceanDevice:
        """Create an EnOcean device based on the provided EEP."""
        pass
