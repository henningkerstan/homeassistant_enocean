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

        # TODO: implement number entities for
        # - min brightness
        # - max brigthness
        # - ramping_time
        #self._number_entitites;

        self._select_entities = [
            HomeAssistantEntityProperties(
            unique_id="ramping_time",
            options=["1s", "2s", "3s", "4s", "5s", "10s"],
            current_option="1s",
            entity_category="diagnostic",
            ),
            HomeAssistantEntityProperties(
            unique_id="min_brightness",
            options=[str(i) for i in range(256)],
            current_option="0",
            entity_category="diagnostic",
            ),
            HomeAssistantEntityProperties(
            unique_id="max_brightness",
            options=[str(i) for i in range(256)],
            current_option="255",
            entity_category="diagnostic",
            ),
        ]


    def handle_matching_packet(self, packet) -> None:
        """Handle an incoming EnOcean packet."""
        
        # ignore non A5 packets
        if packet.rorg != RORG_4BS:
            return
        
        # ignore commands other than 2
        if packet.data[1] != CMD_DIMMING:
            return
        
        # packet.parse_eep(0x38, 0x08)
        # brightness = packet.parsed["EDIM"]["raw_value"]
        # command = packet.parsed["CMD"]["raw_value"]
        # rmp = packet.parsed["RMP"]["raw_value"]
        # edimr = packet.parsed["EDIMR"]["raw_value"]
        # str = packet.parsed["STR"]["raw_value"]
        # sw = packet.parsed["SW"]["raw_value"]

        # print(f"EnOcean A5-38-08 light brightness {brightness}, command {command}, rmp {rmp}, edimr {edimr}, str {str}, sw {sw}")

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

   
        ramping_time = 0x01  # ramp time in seconds
 
        packet = RadioPacket.create(
            rorg=RORG_4BS,
            rorg_func=FUNC,
            rorg_type=0x08,
            command=CMD_DIMMING, # command 2 (set dimmer)
            destination=self.enocean_id.to_bytelist(),
            sender=self.sender_id.to_bytelist(),
            COM=CMD_DIMMING, # command 2 (set dimmer)
            EDIM=brightness,
            RMP=ramping_time,
            EDIMR=0,
            STR=0,
            SW=1
        )
        self.send_packet(packet)
        light_callback = self._light_callbacks.get(None)
        if light_callback:
            light_callback(brightness>0, brightness, 0)

# class EnOceanLight(EnOceanEntity, LightEntity):
#     """Representation of an EnOcean light source."""

#     _attr_color_mode = ColorMode.BRIGHTNESS
#     _attr_supported_color_modes = {ColorMode.BRIGHTNESS}
#     _attr_brightness: int | None = None
#     _attr_is_on = False

#     def __init__(
#         self,
#         sender_id: EnOceanAddress,
#         enocean_entity_id: EnOceanEntityID,
#         gateway: EnOceanHomeAssistantGateway,
#     ) -> None:
#         """Initialize the EnOcean light source."""
#         super().__init__(
#             enocean_entity_id=enocean_entity_id,
#             gateway=gateway,
#         )
#         self._attr_is_on = False
#         self._attr_brightness = None
#         self._sender_id = sender_id
#         self._attr_should_poll = False

#     @property
#     def brightness(self) -> int | None:
#         """Brightness of the light.

#         This method is optional. Removing it indicates to Home Assistant
#         that brightness is not supported for this light.
#         """
#         return self._attr_brightness

#     @property
#     def is_on(self) -> bool | None:
#         """If light is on."""
#         return self._attr_is_on

#     def turn_on(self, **kwargs: Any) -> None:
#         """Turn the light source on or sets a specific dimmer value."""
#         if (brightness := kwargs.get(ATTR_BRIGHTNESS)) is not None:
#             self._attr_brightness = brightness

#         if self._attr_brightness is None:
#             self._attr_brightness = 255
#         bval = math.floor(self._attr_brightness / 256.0 * 100.0)
#         if bval == 0:
#             bval = 1
#         command = [0xA5, 0x02, bval, 0x01, 0x09]
#         command.extend(self._sender_id.to_bytelist())
#         command.extend([0x00])
#         # self.send_command(command, [], 0x01)
#         self._attr_is_on = True

#     def turn_off(self, **kwargs: Any) -> None:
#         """Turn the light source off."""
#         command = [0xA5, 0x02, 0x00, 0x01, 0x09]
#         command.extend(self._sender_id.to_bytelist())
#         command.extend([0x00])
#         #        self.send_command(command, [], 0x01)
#         self._attr_is_on = False

#     def value_changed(self, packet: Packet) -> None:
#         """Update the internal state of this device.

#         Dimmer devices like Eltako FUD61 send telegram in different RORGs.
#         We only care about the 4BS (0xA5).
#         """
#         if packet.data[0] == 0xA5 and packet.data[1] == 0x02:
#             # _LOGGER.info("Received light packet: %s", packet)
#             val = packet.data[2]
#             self._attr_brightness = math.floor(val / 100.0 * 256.0)
#             self._attr_is_on = bool(val != 0)
#             # _LOGGER.info("Setting state to %s", self._attr_is_on)
#             self.schedule_update_ha_state()
