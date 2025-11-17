from homeassistant_enocean.devices.device import EnOceanDevice
from homeassistant_enocean.entity_properties import HomeAssistantEntityProperties


class EnOceanGatewayDevice(EnOceanDevice):

    """Handler for EnOcean Gateway Device"""
    # def __init__(self, enocean_id, send_packet=None, device_name=None, sender_id=None) -> None:
    #     """Initialize the EnOcean Gateway Device."""
    #     super().__init__(enocean_id=enocean_id, send_packet=None, device_name=device_name, sender_id=None)
    #     self.initialize_entities()

    def initialize_entities(self) -> None:
        """Initialize the entities handled by this EEP handler."""
        self.clear_internal_sensor_entities()
        self._button_entities = [
            HomeAssistantEntityProperties(unique_id="learn", entity_category="diagnostic"),
        ]

    def handle_matching_packet(self, packet) -> None:
        """Handle an incoming EnOcean packet."""
        # Gateway device does not handle any specific packets
        pass