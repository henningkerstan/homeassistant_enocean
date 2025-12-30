from homeassistant_enocean.device_type import EnOceanDeviceType
from homeassistant_enocean.devices.device import EnOceanDevice
from homeassistant_enocean.eep import EEP
from homeassistant_enocean.entity_properties import HomeAssistantEntityProperties
from homeassistant_enocean.types import ValueLabelDict


class EnOceanGatewayDevice(EnOceanDevice):

    """Handler for EnOcean Gateway Device"""
    def __init__(self, enocean_id, valid_sender_ids: list[ValueLabelDict] | None = None) -> None:
        """Initialize the EnOcean Gateway Device."""
        self._valid_sender_ids = valid_sender_ids
        super().__init__(enocean_id=enocean_id, send_packet=None, device_type=EnOceanDeviceType(eep=EEP(0, 0, 0), model="TCM300/310 Transmitter", manufacturer="EnOcean"), device_name="Gateway", sender_id=None)
        

    def initialize_entities(self) -> None:
        """Initialize the entities handled by this EEP handler."""
        self.clear_internal_sensor_entities()
        self._button_entities = [
            HomeAssistantEntityProperties(unique_id="start_pairing", entity_category="diagnostic"),
        ]

        valid_sender_ids = []
        if self._valid_sender_ids:
            valid_sender_ids = [option["label"] for option in self._valid_sender_ids]
            
    

        self._binary_sensor_entities = [
            HomeAssistantEntityProperties(unique_id="pairing", entity_category="diagnostic"),
        ]

        self._select_entities = [
            HomeAssistantEntityProperties(unique_id="sender_id", entity_category="diagnostic", options=valid_sender_ids, current_option="Base ID"),
        ]

        self._sensor_entitites = [
            HomeAssistantEntityProperties(unique_id="base_id", entity_category="diagnostic", native_unit_of_measurement=""),
            HomeAssistantEntityProperties(unique_id="pairing_timeout", entity_category="diagnostic", native_unit_of_measurement="s"),
        ]

    def handle_matching_packet(self, packet) -> None:
        """Handle an incoming EnOcean packet."""
        # Gateway device does not handle any specific packets
        pass