from abc import ABC, abstractmethod
from typing import Any, Coroutine

from ..types import EnOceanSendRadioPacket, HomeAssistantTaskCreator
from ..device_type import EnOceanDeviceType
from ..address import EnOceanAddress, EnOceanDeviceAddress
from ..devices.device import EnOceanDevice

class EnOceanDeviceFactory(ABC):
    """Factory class to create EnOcean device handlers based on EEP."""

    def create_device(
            self, 
            enocean_id: EnOceanDeviceAddress, 
            device_type: EnOceanDeviceType, 
            send_packet: EnOceanSendRadioPacket | None = None, 
            device_name: str | None = None, 
            sender_id: EnOceanAddress=None,
            create_task: HomeAssistantTaskCreator | None = None) -> EnOceanDevice:
        """Create an EnOcean device based on the provided EEP."""
        self.__create_task = create_task

        return self._create_device(
            enocean_id=enocean_id,
            device_type=device_type,
            send_packet=send_packet,
            device_name=device_name,
            sender_id=sender_id,
        )

    @abstractmethod
    def _create_device(
            self, 
            enocean_id: EnOceanDeviceAddress, 
            device_type: EnOceanDeviceType, 
            send_packet: EnOceanSendRadioPacket | None = None, 
            device_name: str | None = None, 
            sender_id: EnOceanAddress=None,
    ) -> EnOceanDevice:
        """Create an EnOcean device based on the provided EEP."""
        pass
    

    @property
    def _create_task(self, target: Coroutine[Any, Any, Any]) ->  None:
        """Get the Home Assistant task creator."""
        return self.__create_task(target) if self.__create_task else None
   