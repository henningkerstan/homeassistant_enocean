from ..address import EnOceanAddress, EnOceanDeviceAddress
from .device_factory import EnOceanDeviceFactory
from ..device_type import EnOceanDeviceType
from ..devices.a50801_device import EnOceanA50801Device
from ..eep import EEP
from ..types import EnOceanSendRadioPacket


class EnOceanA50801DeviceFactory(EnOceanDeviceFactory):
    """Factory class to create EnOcean A5-08-01 device handlers based on EEP."""
    def _create_device(self, enocean_id: EnOceanDeviceAddress, device_type: EnOceanDeviceType, send_packet: EnOceanSendRadioPacket | None = None, device_name: str | None = None, sender_id: EnOceanAddress=None) -> EnOceanA50801Device:
        """Create an EnOcean A50801 device handler based on the provided EEP."""
    
        if device_type.eep == EEP(0xA5, 0x08, 0x01):
            return EnOceanA50801Device(enocean_id=enocean_id, device_type=device_type, send_packet=send_packet, device_name=device_name, sender_id=sender_id)
        else:
            raise ValueError(f"EEP {device_type.eep} is not supported by EnOceanA50801DeviceFactory.")