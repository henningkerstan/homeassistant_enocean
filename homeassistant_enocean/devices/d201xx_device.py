# NODON Sin 2-2-01
# https://www.enocean-alliance.org/wp-content/uploads/2017/10/NodOn-SIN-2-2-0x-UserGuide-170731-DE-interactive.pdf



from homeassistant_enocean.devices.device import EnOceanDevice
from homeassistant_enocean.entity_properties import HomeAssistantEntityProperties


class EnOceanD201XXDevice(EnOceanDevice):
    """Handler for EnOcean Equipment Profiles D2-01-00 - D2-01-14"""

    def initialize_entities(self) -> None:
        """Initialize the entities handled by this EEP handler."""
        # D2-01-00 to D2-01-0F have 1 channel, D2-01-10 to D2-01-12 have 2 channels, D2-01-13 has 4 channels, D2-01-14 has 8 channels

        if self.device_type.eep.type in (0x10, 0x11, 0x12):
            self._switch_entities = [
                HomeAssistantEntityProperties(unique_id="switch_1"),
                HomeAssistantEntityProperties(unique_id="switch_2"),
            ]

        elif self.device_type.eep.type == 0x13:
            self._switch_entities = [
                HomeAssistantEntityProperties(unique_id="switch_1"),
                HomeAssistantEntityProperties(unique_id="switch_2"),
                HomeAssistantEntityProperties(unique_id="switch_3"),
                HomeAssistantEntityProperties(unique_id="switch_4"),
            ]
        elif self.device_type.eep.type == 0x14:
            self._switch_entities = [
                HomeAssistantEntityProperties(unique_id="switch_1"),
                HomeAssistantEntityProperties(unique_id="switch_2"),
                HomeAssistantEntityProperties(unique_id="switch_3"),
                HomeAssistantEntityProperties(unique_id="switch_4"),
                HomeAssistantEntityProperties(unique_id="switch_5"),
                HomeAssistantEntityProperties(unique_id="switch_6"),
                HomeAssistantEntityProperties(unique_id="switch_7"),
                HomeAssistantEntityProperties(unique_id="switch_8"),
            ]
        
        else:
            self._switch_entities = [
                HomeAssistantEntityProperties(unique_id=None),
            ]

    def handle_matching_packet(self, packet) -> None:
        """Handle an incoming EnOcean packet."""
        packet.parse_eep(0x01, self.device_type.eep.type)
        if packet.parsed["CMD"]["raw_value"] != 4:
            return
        
        channel = packet.parsed["IO"]["raw_value"]
        output = packet.parsed["OV"]["raw_value"]   

        #print(f"EnOcean D2-01-{self.device_type.eep.type:02X} switch channel {channel} output {output}")

        callback = None 
        if self.device_type.eep.type in (0x10, 0x11, 0x12, 0x13, 0x14):
            callback = self._switch_callbacks.get(f"switch_{channel+1}")
        else:
            callback = self._switch_callbacks.get(None)


        if callback:
            callback(output > 0)

### OUTDATED CODE BELOW ###



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
