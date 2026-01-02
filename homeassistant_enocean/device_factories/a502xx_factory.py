from ..address import EnOceanAddress, EnOceanDeviceAddress
from .device_factory import EnOceanDeviceFactory
from ..device_type import EnOceanDeviceType
from ..devices.a502xx_device import EnOceanA502XXDevice
from ..eep import EEP
from ..types import EnOceanSendRadioPacket


class EnOceanA502XXDeviceFactory(EnOceanDeviceFactory):
    """Factory class to create EnOcean A5-02-XX device handlers based on EEP."""
    def create_device(self, enocean_id: EnOceanDeviceAddress, device_type: EnOceanDeviceType, send_packet: EnOceanSendRadioPacket | None = None, device_name: str | None = None, sender_id: EnOceanAddress=None) -> EnOceanA502XXDevice:
        """Create an EnOcean A502XX device handler based on the provided EEP."""
    
        supported_eeps = [
            EEP(0xA5, 0x02, 0x01),
            EEP(0xA5, 0x02, 0x02),
            EEP(0xA5, 0x02, 0x03),
            EEP(0xA5, 0x02, 0x04),
            EEP(0xA5, 0x02, 0x05),
            EEP(0xA5, 0x02, 0x06),
            EEP(0xA5, 0x02, 0x07),
            EEP(0xA5, 0x02, 0x08),
            EEP(0xA5, 0x02, 0x09),
            EEP(0xA5, 0x02, 0x0A),
            EEP(0xA5, 0x02, 0x0B),
    
            EEP(0xA5, 0x02, 0x10),
            EEP(0xA5, 0x02, 0x11),
            EEP(0xA5, 0x02, 0x12),
            EEP(0xA5, 0x02, 0x13),
            EEP(0xA5, 0x02, 0x14),
            EEP(0xA5, 0x02, 0x15),
            EEP(0xA5, 0x02, 0x16),
            EEP(0xA5, 0x02, 0x17),
            EEP(0xA5, 0x02, 0x18),
            EEP(0xA5, 0x02, 0x19),
            EEP(0xA5, 0x02, 0x1A),
            EEP(0xA5, 0x02, 0x1B)
        ]

        if device_type.eep in supported_eeps:
            return EnOceanA502XXDevice(enocean_id=enocean_id, device_type=device_type, send_packet=send_packet, device_name=device_name, sender_id=sender_id)
        else:
            raise ValueError(f"EEP {device_type.eep} is not supported by EnOceanA502XXDeviceFactory.")