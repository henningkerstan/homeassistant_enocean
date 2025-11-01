#   # position is inversed in Home Assistant and in EnOcean:
#         # 0 means 'closed' in Home Assistant and 'open' in EnOcean
#         # 100 means 'open' in Home Assistant and 'closed' in EnOcean

#         new_position = 100 - packet.data[1]

#         if self._position is not None:
#             if self._state_changed_by_command:
#                 self._state_changed_by_command = False

#             elif new_position in (0, 100):
#                 self._is_opening = False
#                 self._is_closing = False
#                 self.stop_watchdog()

#             elif new_position == self._position:
#                 if self._stop_suspected:
#                     self._stop_suspected = False
#                     self._is_opening = False
#                     self._is_closing = False
#                     self.stop_watchdog()
#                 else:
#                     self.start_or_feed_watchdog()
#                     self._stop_suspected = True
#                     return

#             elif new_position > self._position:
#                 self._is_opening = True
#                 self._is_closing = False
#                 self.start_or_feed_watchdog()

#             elif new_position < self._position:
#                 self._is_opening = False
#                 self._is_closing = True
#                 self.start_or_feed_watchdog()

#         self._position = new_position
#         if self._position == 0:
#             self._attr_is_closed = True
#         else:
#             self._attr_is_closed = False

class EEP_D2_05_00_Handler(EEPHandler):
    """Handler for EnOcean Equipment Profile D2-05-00"""

    
    def handle_packet_matching(self, packet: RadioPacket, device_state: EnOceanDeviceProperties) -> list[EnOceanEntityID]:
        """Handle an incoming EnOcean packet."""
        contact_status = packet.data[0] & 0x01

        if contact_status == 0x00:
            device_state.binary_sensor_is_on["contact"] = False
        else:
            device_state.binary_sensor_is_on["contact"] = True

        return [EnOceanEntityID(device_state.enocean_id, "contact")]