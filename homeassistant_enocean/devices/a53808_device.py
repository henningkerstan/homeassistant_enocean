import math

from homeassistant_enocean.types import EnOceanEntityUID
from .device import EnOceanDevice
from ..entity_properties import HomeAssistantEntityProperties
from enocean.protocol.packet import RadioPacket

RORG_4BS = 0xA5
FUNC = 0x38
CMD_DIMMING = 0x02

class EnOceanA53808Device(EnOceanDevice):
    """Handler for EnOcean Equipment Profile A5-38-08 (Gateway)"""

    def initialize_entities(self) -> None:
        """Initialize the entities handled by this EEP handler."""
        self._light_entities = [
            HomeAssistantEntityProperties(unique_id=None, device_class="light"),
        ]

        self._number_entities = [
            HomeAssistantEntityProperties(
                unique_id="ramping_time",
                native_min_value=0,
                native_max_value=255,
                native_step=1,
                native_value=1,
                entity_category="diagnostic",
                native_unit_of_measurement="s",
                device_class="duration"
            ),
            HomeAssistantEntityProperties(
                unique_id="min_brightness",
                native_min_value=0,
                native_max_value=255,
                native_step=1,
                native_value=0,
                entity_category="diagnostic",
                native_unit_of_measurement=""
            ),
            HomeAssistantEntityProperties(
                unique_id="max_brightness",
                native_min_value=0,
                native_max_value=255,
                native_step=1,
                native_value=255,
                entity_category="diagnostic",
                native_unit_of_measurement=""
            ),
        ]


    def handle_matching_packet(self, packet) -> None:
        """Handle an incoming EnOcean packet."""

        # ignore non A5 packets
        if packet.rorg != RORG_4BS:
            return
        
        # ignore commands other than 2
        com = packet.data[1]
        if com != CMD_DIMMING:
            return
        
        # try:
        #     packet.parse_eep(0x38, 0x08, 2)
        #     brightness = packet.parsed["EDIM"]["raw_value"]
        #     rmp = packet.parsed["RMP"]["raw_value"]
        #     edimr = packet.parsed["EDIMR"]["raw_value"]
        #     str = packet.parsed["STR"]["raw_value"]
        #     sw = packet.parsed["SW"]["raw_value"]

        #     print(f"EnOcean A5-38-08 light brightness {brightness}, command {com}, rmp {rmp}, edimr {edimr}, str {str}, sw {sw}")

        # except Exception as e:
        #     print(f"Error parsing A5-38-08 packet: {e}")
        #     print(f"Packet: {packet}")

        
        brightness_percentage = packet.data[2]
        brightness = math.floor(brightness_percentage / 100.0 * 256.0)

        light_callback = self._light_callbacks.get(None)
        if light_callback:
            light_callback(brightness>0, brightness, 0)

    def light_turn_off(self, entity_uid: EnOceanEntityUID) -> None:
        """Turn the light source off."""
        ramping_time = 0x01  # ramp time in seconds
        packet = RadioPacket.create(
            rorg=RORG_4BS,
            rorg_func=FUNC,
            rorg_type=0x08,
            command=CMD_DIMMING, # command 2 (set dimmer)
            destination=self.enocean_id.to_bytelist(),
            sender=self.sender_id.to_bytelist(),
            COM=CMD_DIMMING, # command 2 (set dimmer)
            EDIM=0,
            RMP=ramping_time,
            EDIMR=0,
            STR=0,
            SW=0
        )
        self.send_packet(packet)

        light_callback = self._light_callbacks.get(None)
        if light_callback:
            light_callback(False, 0, 0)
    

    def light_turn_on(self, entity_uid: EnOceanEntityUID, brightness: int | None = None, color_temp_kelvin: int | None = None) -> None:
        """Turn the light source on or sets a specific dimmer value."""
        if brightness is None:
            brightness = 255

        brightness_percentage = math.floor(brightness / 256.0 * 100.0)
   
        ramping_time = 0x01  # ramp time in seconds
 
        packet = RadioPacket.create(
            rorg=RORG_4BS,
            rorg_func=FUNC,
            rorg_type=0x08,
            command=CMD_DIMMING, # command 2 (set dimmer)
            destination=self.enocean_id.to_bytelist(),
            sender=self.sender_id.to_bytelist(),
            COM=CMD_DIMMING, # command 2 (set dimmer)
            EDIM=brightness_percentage,
            RMP=ramping_time,
            EDIMR=1,
            STR=0,
            SW=1
        )
        self.send_packet(packet)
        light_callback = self._light_callbacks.get(None)
        if light_callback:
            light_callback(brightness>0, brightness, 0)

    def set_number_value(self, entity_uid: EnOceanEntityUID, value: float) -> None:
        """Set the value of a number entity."""
        int_value = int(value)
        if int_value < 0:
            int_value = 0
        elif int_value > 255:
            int_value = 255

        if entity_uid in ("min_brightness", "max_brightness"):
           self.light_turn_on(entity_uid=None, brightness=int_value)