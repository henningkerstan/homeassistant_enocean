from ..address import EnOceanAddress, EnOceanDeviceAddress
from ..device_type import EnOceanDeviceType
from ..devices.f61000_device import EnOceanF61000Device
from ..eep import EEP
from ..types import EnOceanSendRadioPacket, HomeAssistantTaskCreator
from .device_factory import EnOceanDeviceFactory


class EnOceanF61000DeviceFactory(EnOceanDeviceFactory):
    """Factory class to create EnOcean F61000 devices based on EEP."""

    def create_device(
        self,
        enocean_id: EnOceanDeviceAddress,
        device_type: EnOceanDeviceType,
        send_packet: EnOceanSendRadioPacket | None = None,
        device_name: str | None = None,
        sender_id: EnOceanAddress | None = None,
        create_task: HomeAssistantTaskCreator | None = None,
    ) -> EnOceanF61000Device:
        """Create an EnOcean F61000 device based on the provided EEP."""

        if device_type.eep == EEP(0xF6, 0x10, 0x00):
            return EnOceanF61000Device(
                enocean_id=enocean_id,
                device_type=device_type,
                create_task=create_task,
                send_packet=send_packet,
                device_name=device_name,
                sender_id=sender_id,
            )
        else:
            raise ValueError(
                f"EEP {device_type.eep} is not supported by EnOceanF61000DeviceFactory."
            )
