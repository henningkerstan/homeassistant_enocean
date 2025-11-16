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