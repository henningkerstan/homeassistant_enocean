# NODON Sin 2-2-01
# https://www.enocean-alliance.org/wp-content/uploads/2017/10/NodOn-SIN-2-2-0x-UserGuide-170731-DE-interactive.pdf



from homeassistant_enocean.eep_handlers.eep_handler import EEPHandler
from homeassistant_enocean.entity_properties import HomeAssistantEntityProperties


class EEP_D2_01_Handler(EEPHandler):
    """Handler for EnOcean Equipment Profiles D2-01-00 - D2-01-14"""

    def  initialize_entities(self) -> None:
        """Initialize the entities handled by this EEP handler."""
        # todo: support multiple channels,
        # for now, we assume only 2 channels per device
        # D2-01-00 to D2-01-0F have 1 channel, D2-01-10 to D2-01-12 have 2 channels, D2-01-13 has 4 channels, D2-01-14 has 8 channels
        self._switch_entities = [
            HomeAssistantEntityProperties(unique_id="channel_1"),
            HomeAssistantEntityProperties(unique_id="channel_2"),
        ]

    def handle_matching_packet(self, packet, enocean_id, sender_id) -> None:
        """Handle an incoming EnOcean packet."""

        # if packet.data[0] == 0xA5:
        #     # power meter telegram, turn on if > 10 watts
        #     packet.parse_eep(0x12, 0x01)
        #     if packet.parsed["DT"]["raw_value"] == 1:
        #         raw_val = packet.parsed["MR"]["raw_value"]
        #         divisor = packet.parsed["DIV"]["raw_value"]
        #         watts = raw_val / (10**divisor)
        #         if watts > 1:
        #             self._attr_is_on = True
        #             self.schedule_update_ha_state()
        # elif packet.data[0] == 0xD2:
        
        # actuator status telegram
        packet.parse_eep(0x01, 0x01)
        if packet.parsed["CMD"]["raw_value"] != 4:
            return
        
        channel = packet.parsed["IO"]["raw_value"]
        output = packet.parsed["OV"]["raw_value"]    

        callback = self._switch_callbacks.get(f"channel_{channel+1}")
        if callback:
            callback(output > 0)

### OUTDATED CODE BELOW ###


# class EnOceanSwitchOLD(EnOceanEntity, SwitchEntity):
#     """Representation of an EnOcean switch device."""

#     def __init__(
#         self,
#         enocean_entity_id: EnOceanEntityID,
#         gateway: EnOceanHomeAssistantGateway,
#         channel: int,
#         dev_type: EnOceanDeviceType,
#         name: str | None = None,
#     ) -> None:
#         """Initialize the EnOcean switch device."""
#         super().__init__(
#             enocean_entity_id=enocean_entity_id,
#             gateway=gateway,
#         )
#         self._light = None
#         self.channel = channel

#     @property
#     def is_on(self) -> bool | None:
#         """Return whether the switch is on or off."""
#         return self._attr_is_on

#     def turn_on(self, **kwargs: Any) -> None:
#         """Turn on the switch."""
#         optional = [0x03]
#         optional.extend(self.__enocean_entity_id.to_bytelist())
#         optional.extend([0xFF, 0x00])
#         # self.send_command(
#         #     data=[0xD2, 0x01, self.channel & 0xFF, 0x64, 0x00, 0x00, 0x00, 0x00, 0x00],
#         #     optional=optional,
#         #     packet_type=0x01,
#         # )
#         self._attr_is_on = True

#     def turn_off(self, **kwargs: Any) -> None:
#         """Turn off the switch."""
#         optional = [0x03]
#         optional.extend(self.__enocean_entity_id.to_bytelist())
#         optional.extend([0xFF, 0x00])
#         # self.send_command(
#         #     data=[0xD2, 0x01, self.channel & 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
#         #     optional=optional,
#         #     packet_type=0x01,
#         # )
#         self._attr_is_on = False

#     def value_changed(self, packet: Packet) -> None:
#         """Update the internal state of the switch."""
#         if packet.data[0] == 0xA5:
#             # power meter telegram, turn on if > 10 watts
#             packet.parse_eep(0x12, 0x01)
#             if packet.parsed["DT"]["raw_value"] == 1:
#                 raw_val = packet.parsed["MR"]["raw_value"]
#                 divisor = packet.parsed["DIV"]["raw_value"]
#                 watts = raw_val / (10**divisor)
#                 if watts > 1:
#                     self._attr_is_on = True
#                     self.schedule_update_ha_state()
#         elif packet.data[0] == 0xD2:
#             # actuator status telegram
#             packet.parse_eep(0x01, 0x01)
#             if packet.parsed["CMD"]["raw_value"] == 4:
#                 channel = packet.parsed["IO"]["raw_value"]
#                 output = packet.parsed["OV"]["raw_value"]
#                 if channel == self.channel:
#                     self._attr_is_on = output > 0
#                     self.schedule_update_ha_state()
