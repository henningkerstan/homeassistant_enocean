from dataclasses import dataclass

from homeassistant_enocean.address import EnOceanDeviceAddress

from .esp3 import ESP3Packet
from .types import RORG


class ERP1ParseError(Exception):
    pass


@dataclass
class ERP1:
    rorg: RORG
    payload: bytes
    sender: EnOceanDeviceAddress
    status: int

    sub_tel_num: int
    dBm: int
    sec_level: int

    @classmethod
    def from_esp3(cls, pkt: ESP3Packet):
        if pkt.packet_type != 0x01:
            raise ERP1ParseError("Not an ERP1 packet")

        data = pkt.data
        opt = pkt.optional

        # --- Sanity checks ---
        if len(data) < 6:
            raise ERP1ParseError(f"ERP1 telegram too short: {len(data)} bytes")

        if len(opt) < 3:
            raise ERP1ParseError(f"ERP1 optional data too short: {len(opt)} bytes")

        # --- Parse DATA ---
        try:
            rorg = RORG(data[0])
        except ValueError:
            raise ERP1ParseError(f"Unknown RORG: 0x{data[0]:02X}")

        sender = data[-5:-1]
        status = data[-1]
        payload = data[1:-5]

        # --- Parse OPTIONAL ---
        sub_tel_num = opt[0]
        dBm = opt[1]
        sec_level = opt[2]

        return cls(
            rorg=rorg,
            payload=payload,
            sender=sender,
            status=status,
            sub_tel_num=sub_tel_num,
            dBm=dBm,
            sec_level=sec_level,
        )
