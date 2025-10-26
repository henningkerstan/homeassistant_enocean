from home_assistant_enocean.device_properties import EnOceanDeviceProperties
from home_assistant_enocean.entity import EnOceanEntity
from .eep_handler import EEPHandler
from enocean.protocol.packet import RadioPacket

class EEP_F6_02_Handler(EEPHandler):
    """Handler for EnOcean Equipment Profiles F6-02-01/02"""

    def binary_sensor_entities(self):
        return ["A0", "A1", "B0", "B1", "AB0", "AB1", "A0B1", "A1B0"]

    def handle_packet_matching(self, packet: RadioPacket, device_state: EnOceanDeviceProperties) -> list[EnOceanEntity]:
        """Handle an incoming EnOcean packet."""
        action = packet.data[1]

        print(f"Handling F6-02 packet with action: 0x{action:02X}")

        match action:
            case 0x70:
                device_state.binary_sensor_is_on["A0"] = True
                return [EnOceanEntity(device_state.enocean_id, "A0")]

            case 0x50:
                device_state.binary_sensor_is_on["A1"] = True
                return [EnOceanEntity(device_state.enocean_id, "A1")]

            case 0x30:
                device_state.binary_sensor_is_on["B0"] = True
                return [EnOceanEntity(device_state.enocean_id, "B0")]

            case 0x10:
                device_state.binary_sensor_is_on["B1"] = True
                return [EnOceanEntity(device_state.enocean_id, "B1")]

            case 0x37:
                device_state.binary_sensor_is_on["AB0"] = True
                return [EnOceanEntity(device_state.enocean_id, "AB0")]

            case 0x15:
                device_state.binary_sensor_is_on["AB1"] = True
                return [EnOceanEntity(device_state.enocean_id, "AB1")]

            case 0x17:
                device_state.binary_sensor_is_on["A0B1"] = True
                return [EnOceanEntity(device_state.enocean_id, "A0B1")]

            case 0x35:
                device_state.binary_sensor_is_on["A1B0"] = True
                return [EnOceanEntity(device_state.enocean_id, "A1B0")]

        
            case 0x00:
                if device_state.binary_sensor_is_on.get("A0"):
                    device_state.binary_sensor_is_on["A0"] = False

       