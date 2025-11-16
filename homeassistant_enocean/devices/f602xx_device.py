from homeassistant_enocean.address import EnOceanAddress, EnOceanDeviceAddress
from homeassistant_enocean.devices.device import EnOceanDevice
from homeassistant_enocean.entity_properties import HomeAssistantEntityProperties
from homeassistant_enocean.types import EnOceanBinarySensorCallback
from enocean.protocol.packet import RadioPacket

class EnOceanF602XXDevice(EnOceanDevice):
    """Handler for EnOcean Equipment Profiles F6-02-01/02"""
    
    def initialize_entities(self) -> None:
        """Initialize the entities handled by this EEP handler."""
        self._binary_sensor_entities = [
            HomeAssistantEntityProperties(unique_id="a0",),
            HomeAssistantEntityProperties(unique_id="a1"),
            HomeAssistantEntityProperties(unique_id="b0"),
            HomeAssistantEntityProperties(unique_id="b1"),
            HomeAssistantEntityProperties(unique_id="ab0"),
            HomeAssistantEntityProperties(unique_id="ab1"),
            HomeAssistantEntityProperties(unique_id="a0b1"),
            HomeAssistantEntityProperties(unique_id="a1b0"),
        ]
    

    def handle_matching_packet(self, packet: RadioPacket, enocean_id: EnOceanDeviceAddress, sender_id: EnOceanAddress) -> None:
        """Handle an incoming EnOcean packet."""
        action = packet.data[1]
        print(f"EEP_F602XX: Handling packet with action {action:#04x} for device ID {enocean_id.to_string()}")

        if action == 0x00:
            for callback in self._binary_sensor_callbacks.values():
                callback(False)

        callback : EnOceanBinarySensorCallback | None = None

        match action:
            case 0x70:
                callback = self._binary_sensor_callbacks.get("a0")
            case 0x50:
                callback = self._binary_sensor_callbacks.get("a1")
            case 0x30:
                callback = self._binary_sensor_callbacks.get("b0")
            case 0x10:
                callback = self._binary_sensor_callbacks.get("b1") 
            case 0x37:
                callback = self._binary_sensor_callbacks.get("ab0")
            case 0x15:
                callback = self._binary_sensor_callbacks.get("ab1")
            case 0x17:
                callback = self._binary_sensor_callbacks.get("a0b1")
            case 0x35:
                callback = self._binary_sensor_callbacks.get("a1b0")

        if callback:
            callback(True)
