from enum import IntEnum


class ESP3PacketType(IntEnum):
    RADIO_ERP1 = 0x01
    RESPONSE = 0x02
    RADIO_SUB_TEL = 0x03
    EVENT = 0x04
    COMMON_COMMAND = 0x05
    SMART_ACK_COMMAND = 0x06
    REMOTE_MAN_COMMAND = 0x07
    RADIO_MESSAGE = 0x09
    RADIO_ERP2 = 0x0A


class RORG(IntEnum):
    RPS = 0xF6
    ONEBS = 0xD5
    FOURBS = 0xA5
    VLD = 0xD2
    UTE = 0xD4
