# PIR NODON

from homeassistant_enocean.eep_handlers.eep_handler import EEPHandler
from homeassistant_enocean.entity_properties import HomeAssistantEntityProperties


class EEP_A5_07_03_Handler(EEPHandler):
    """Handler for EnOcean Equipment Profile A5-07-03 (PIR NODON)"""

    def initialize_entities(self) -> None:
        """Initialize the entities handled by this EEP handler."""
        self._binary_sensor_entities = [
            HomeAssistantEntityProperties(unique_id="motion_detected", device_class="motion"),
        ]

        self._sensor_entitites = [
            HomeAssistantEntityProperties(unique_id="supply_voltage", device_class="voltage", entity_category="diagnostic"),
            HomeAssistantEntityProperties(unique_id="illumination", native_unit_of_measurement="lx", device_class="illuminance"),
        ]

    def handle_matching_packet(self, packet, enocean_id, sender_id) -> None:
        """Handle an incoming EnOcean packet."""
        packet.parse_eep(0x07, 0x03)
        motion = packet.parsed["PIRS"]["raw_value"]
        illumination = packet.parsed["ILL"]["raw_value"]
        supply_voltage = 5.0 * (packet.parsed["SVC"]["raw_value"]/250.0)  # convert to volts from range 0..250 representing 0..5V

        motion_callback = self._binary_sensor_callbacks.get("motion_detected")
        if motion_callback:
            motion_callback(motion)

        illumination_callback = self._sensor_callbacks.get("illumination")
        if illumination_callback:
            illumination_callback(illumination)

        supply_voltage_callback = self._sensor_callbacks.get("supply_voltage")
        if supply_voltage_callback:
            supply_voltage_callback(supply_voltage)