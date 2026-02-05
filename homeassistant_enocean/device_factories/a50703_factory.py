from ..address import EURID, EnOceanAddress
from ..device_type import EnOceanDeviceType
from ..devices.a50703_device import EnOceanA50703Device
from ..eep import EEP
from ..types import EnOceanSendRadioPacket, HomeAssistantTaskCreator
from .device_factory import EnOceanDeviceFactory


class EnOceanA50703DeviceFactory(EnOceanDeviceFactory):
    """Factory class to create EnOcean A5-07-03 devices based on EEP."""

    def create_device(
        self,
        enocean_id: EURID,
        device_type: EnOceanDeviceType,
        send_packet: EnOceanSendRadioPacket | None = None,
        device_name: str | None = None,
        sender_id: EnOceanAddress = None,
        create_task: HomeAssistantTaskCreator | None = None,
    ) -> EnOceanA50703Device:
        """Create an EnOcean A50703 device based on the provided EEP."""

        if device_type.eep == EEP(0xA5, 0x07, 0x03):
            return EnOceanA50703Device(
                enocean_id=enocean_id,
                device_type=device_type,
                create_task=create_task,
                send_packet=send_packet,
                device_name=device_name,
                sender_id=sender_id,
            )
        else:
            raise ValueError(
                f"EEP {device_type.eep} is not supported by EnOceanA50703DeviceFactory."
            )
