from homeassistant_enocean.types import EnOceanSendRadioPacket
from ..address import EnOceanAddress, EnOceanDeviceAddress
from .device_factory import EnOceanDeviceFactory
from ..device_type import EnOceanDeviceType
from ..devices.d20500_device import EnOceanD20500Device
from ..eep import EEP

class EnOceanD20500DeviceFactory(EnOceanDeviceFactory):
    """Factory class to create EnOcean D20500 device handlers based on EEP."""
    def _create_device(self, enocean_id: EnOceanDeviceAddress, device_type: EnOceanDeviceType, send_packet: EnOceanSendRadioPacket | None = None, device_name: str | None = None, sender_id: EnOceanAddress=None) -> EnOceanD20500Device:
        """Create an EnOcean D20500 device handler based on the provided EEP."""

        if device_type.eep == EEP(0xD2, 0x05, 0x00):
            return EnOceanD20500Device(enocean_id=enocean_id, device_type=device_type, send_packet=send_packet, device_name=device_name, sender_id=sender_id)
        else:
            raise ValueError(f"EEP {device_type.eep} is not supported by EnOceanD20500DeviceFactory.")