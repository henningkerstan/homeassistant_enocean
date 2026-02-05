from dataclasses import dataclass

from .types import PacketType


@dataclass
class ESP3Packet:
    """
    Represents a raw ESP3 packet.

    This class does NOT interpret radio payloads.
    It only stores the ESP3 structure:
      - packet type
      - data bytes
      - optional bytes
    """

    packet_type: PacketType
    data: bytes
    optional: bytes

    @property
    def data_length(self) -> int:
        return len(self.data)

    @property
    def optional_length(self) -> int:
        return len(self.optional)

    def __repr__(self) -> str:
        return (
            f"ESP3Packet(type=0x{self.packet_type.name}, "
            f"data={self.data.hex()}, "
            f"optional={self.optional.hex()})"
        )
