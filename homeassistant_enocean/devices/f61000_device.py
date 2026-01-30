from .device import EnOceanDevice
from ..entity_properties import HomeAssistantEntityProperties
from ..types import EnOceanSensorCallback
from enocean.protocol.packet import RadioPacket


class EnOceanF61000Device(EnOceanDevice):
    """Handler for EnOcean Equipment Profiles F6-10-00 (Window Handle)"""

    def initialize_entities(self) -> None:
        """Initialize the entities handled by this EEP handler."""
        self._sensor_entities = [
            HomeAssistantEntityProperties(
                unique_id=None,
                device_class="enum",
                options=[
                    "up2vertical",
                    "vertical2up",
                    "down2vertical",
                    "vertical2down",
                ],
            ),
        ]

    def handle_matching_packet(self, packet: RadioPacket) -> None:
        """Handle an incoming EnOcean packet."""
        action = None

        try:
            packet.parse_eep(rorg_func=0x10, rorg_type=0x00)
            win = packet.parsed["WIN"]["value"]

            match win:
                case 0x00:
                    action = "up2vertical"
                case 0x01:
                    action = "vertical2up"
                case 0x02:
                    action = "down2vertical"
                case 0x03:
                    action = "vertical2down"

        except Exception:
            return

        if action is None:
            return

        callback: EnOceanSensorCallback | None = None
        callback = self._sensor_callbacks.get(None)

        if callback:
            callback(action)
