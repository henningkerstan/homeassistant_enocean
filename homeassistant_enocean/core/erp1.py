from dataclasses import dataclass
from enum import IntEnum

from homeassistant_enocean.core.address import EURID, EnOceanBroadcastAddress

from .esp3 import ESP3Packet, ESP3PacketType


class RORG(IntEnum):
    RPS = 0xF6
    ONEBS = 0xD5
    FOURBS = 0xA5
    VLD = 0xD2
    UTE = 0xD4


class ERP1ParseError(Exception):
    pass


@dataclass
class ERP1Telegram:
    rorg: RORG
    payload: bytes
    sender: EURID
    status: int

    sub_tel_num: int | None = None
    dBm: int | None = None
    sec_level: int | None = None

    destination: EURID | EnOceanBroadcastAddress | None = None

    @classmethod
    def from_esp3(cls, pkt: ESP3Packet):
        if pkt.packet_type != ESP3PacketType.RADIO_ERP1:
            raise ERP1ParseError("Not an ERP1 telegram")

        data = pkt.data
        opt = pkt.optional

        # --- Sanity checks ---
        if len(data) < 6:
            raise ERP1ParseError(f"ERP1 telegram too short: {len(data)} bytes")

        # --- Parse DATA ---
        try:
            rorg = RORG(data[0])
        except ValueError:
            raise ERP1ParseError(f"Unknown RORG: 0x{data[0]:02X}")

        sender = EURID.from_bytelist(data[-5:-1])
        status = data[-1]
        payload = data[1:-5]

        # --- Parse OPTIONAL ---
        sub_tel_num = opt[0] if len(opt) > 0 else None
        dBm = opt[1] if len(opt) > 1 else None
        sec_level = opt[2] if len(opt) > 2 else None
        destination_bytes = opt[3:8] if len(opt) > 7 else None

        return cls(
            rorg=rorg,
            payload=payload,
            sender=sender,
            status=status,
            sub_tel_num=sub_tel_num,
            dBm=dBm,
            sec_level=sec_level,
        )


@dataclass
class CommonCommandTelegram:
    """Common Command Telegram for ESP3 packets."""

    common_command_code: int
    common_command_data: bytes | None = None
    optional_data: bytes = None

    def __post_init__(self):
        if self.optional_data is None:
            self.optional_data = b""

    def to_esp3_packet(self) -> ESP3Packet:
        data_size = (
            1 if self.common_command_data is None else len(self.common_command_data) + 1
        )
        data = bytearray(data_size)
        data[0] = self.common_command_code

        if self.common_command_data is not None:
            data[1:] = self.common_command_data

        return ESP3Packet(
            packet_type=ESP3PacketType.COMMON_COMMAND,
            data=bytes(data),
            optional=self.optional_data,
        )

    @classmethod
    def from_esp3_packet(cls, packet: ESP3Packet) -> "CommonCommandTelegram":
        if packet.packet_type != ESP3PacketType.COMMON_COMMAND:
            raise ERP1ParseError("ESP3Packet is not a common command telegram")

        if len(packet.optional) > 0:
            raise ERP1ParseError(
                "ESP3Packet is not a valid common command; optional data is present"
            )

        if len(packet.data) < 1:
            raise ERP1ParseError("ESP3Packet is not a valid common command; no data")

        common_command_code = packet.data[0]
        common_command_data = packet.data[1:] if len(packet.data) > 1 else None

        return cls(common_command_code, common_command_data)
