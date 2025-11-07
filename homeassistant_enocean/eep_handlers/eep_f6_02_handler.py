from home_assistant_enocean.device_state import EnOceanDeviceState
from home_assistant_enocean.entity_id import EnOceanEntityID
from .eep_handler import EEPHandler
from enocean.protocol.packet import RadioPacket

class EEP_F6_02_Handler(EEPHandler):
    """Handler for EnOcean Equipment Profiles F6-02-01/02"""

    def binary_sensor_entities(self):
        return {"a0": False, "a1": False, "b0": False, "b1": False, "ab0": False, "ab1": False, "a0b1": False, "a1b0": False}

    def handle_packet_matching(self, packet: RadioPacket, device_state: EnOceanDeviceState) -> list[EnOceanEntityID]:
        """Handle an incoming EnOcean packet."""
        action = packet.data[1]

        match action:
            case 0x70:
                device_state.binary_sensor_is_on["a0"] = True
                return [EnOceanEntityID(device_state.enocean_id, "a0")]

            case 0x50:
                device_state.binary_sensor_is_on["a1"] = True
                return [EnOceanEntityID(device_state.enocean_id, "a1")]

            case 0x30:
                device_state.binary_sensor_is_on["b0"] = True
                return [EnOceanEntityID(device_state.enocean_id, "b0")]

            case 0x10:
                device_state.binary_sensor_is_on["b1"] = True
                return [EnOceanEntityID(device_state.enocean_id, "b1")]

            case 0x37:
                device_state.binary_sensor_is_on["ab0"] = True
                return [EnOceanEntityID(device_state.enocean_id, "ab0")]

            case 0x15:
                device_state.binary_sensor_is_on["ab1"] = True
                return [EnOceanEntityID(device_state.enocean_id, "ab1")]

            case 0x17:
                device_state.binary_sensor_is_on["a0b1"] = True
                return [EnOceanEntityID(device_state.enocean_id, "a0b1")]

            case 0x35:
                device_state.binary_sensor_is_on["a1b0"] = True
                return [EnOceanEntityID(device_state.enocean_id, "a1b0")]

        
            case 0x00:
                entities_affected = []
                for name in self.binary_sensor_entities():
                    if device_state.binary_sensor_is_on.get(name, False):
                        device_state.binary_sensor_is_on[name] = False
                        entities_affected.append(EnOceanEntityID(device_state.enocean_id, name))
                return entities_affected

       