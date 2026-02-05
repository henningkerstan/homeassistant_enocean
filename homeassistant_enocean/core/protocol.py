import asyncio
from typing import Callable

import serial_asyncio_fast as serial_asyncio

from .erp1 import RORG, ERP1Telegram
from .esp3 import SYNC_BYTE, ESP3Packet, ESP3PacketType, crc8

type PacketCallback = Callable[[ESP3Packet], None]
type ERP1Callback = Callable[[ERP1Telegram], None]
# type UTECallback = Callable[[UTE], None]


class EnOceanProtocol(asyncio.Protocol):
    """
    Minimal asynchronous EnOcean ESP3 gateway.
    - Parses ESP3 frames
    - Emits raw ESP3 packets
    - Emits ERP1 telegrams
    - Emits UTE teach-in telegrams
    """

    def __init__(self):
        self.transport = None
        self._buffer = bytearray()

        # Raw ESP3 packet callbacks
        self._packet_callbacks: list[PacketCallback] = []

        # ERP1 callbacks
        self._erp1_callbacks: list[ERP1Callback] = []

        # UTE callbacks
        # self._ute_callbacks: list[UTECallback] = []

    @classmethod
    async def open_serial_port(
        cls, port: str, baudrate: int = 57600
    ) -> "EnOceanProtocol":
        """Open a serial connection to the EnOcean gateway and return an instance of EnOceanProtocol."""
        loop = asyncio.get_running_loop()
        protocol = cls()

        try:
            await serial_asyncio.create_serial_connection(
                loop, lambda: protocol, port, baudrate=baudrate
            )
        except Exception as e:
            raise ConnectionError(
                f"Failed to connect to EnOcean gateway on {port}: {e}"
            )

        return protocol

    # ------------------------------------------------------------------
    # Callback registration
    # ------------------------------------------------------------------

    def add_packet_callback(self, cb: PacketCallback):
        self._packet_callbacks.append(cb)

    def add_erp1_callback(self, cb: ERP1Callback):
        self._erp1_callbacks.append(cb)

    # ------------------------------------------------------------------
    # Emit helpers
    # ------------------------------------------------------------------

    def _emit(self, callbacks, obj):
        loop = asyncio.get_running_loop()
        for cb in callbacks:
            loop.call_soon(cb, obj)

    # ------------------------------------------------------------------
    # Serial protocol
    # ------------------------------------------------------------------

    def connection_made(self, transport: serial_asyncio.SerialTransport):
        self.transport = transport

    def data_received(self, data: bytes):
        self._buffer.extend(data)
        self._process_buffer()

    def connection_lost(self, exc):
        self.transport = None

    def eof_received(self, exc):
        pass

    # ------------------------------------------------------------------
    # ESP3 framing + parsing
    # ------------------------------------------------------------------

    def _process_buffer(self):
        while True:
            # Find sync byte
            try:
                sync_index = self._buffer.index(SYNC_BYTE)
            except ValueError:
                self._buffer.clear()
                return

            # Drop garbage before sync
            if sync_index > 0:
                del self._buffer[:sync_index]

            # Need at least sync + header + header CRC
            if len(self._buffer) < 6:
                return

            header = self._buffer[1:5]
            data_len = (header[0] << 8) | header[1]
            opt_len = header[2]
            packet_type = header[3]

            total_len = 1 + 4 + 1 + data_len + opt_len + 1
            if len(self._buffer) < total_len:
                return

            # Validate header CRC
            if self._buffer[5] != crc8(header):
                del self._buffer[:1]
                continue

            # Extract data + optional
            data_start = 6
            data_end = data_start + data_len
            opt_end = data_end + opt_len

            data = bytes(self._buffer[data_start:data_end])
            optional = bytes(self._buffer[data_end:opt_end])

            # Validate data CRC
            if self._buffer[opt_end] != crc8(data + optional):
                del self._buffer[:1]
                continue

            pkt = ESP3Packet(ESP3PacketType(packet_type), data, optional)

            # Emit raw ESP3 packet
            self._emit(self._packet_callbacks, pkt)

            # Handle ERP1
            if pkt.packet_type == ESP3PacketType.RADIO_ERP1:
                rorg_byte = data[0]

                # UTE teach-in
                if rorg_byte == RORG.UTE:
                    # try:
                    #     ute = UTE.from_esp3(pkt)
                    #     self._emit(self._ute_callbacks, ute)
                    # except Exception:
                    #     pass
                    pass

                # Normal ERP1 telegram
                else:
                    try:
                        erp1 = ERP1Telegram.from_esp3(pkt)
                        self._emit(self._erp1_callbacks, erp1)
                    except Exception:
                        pass

            # Remove processed bytes
            del self._buffer[:total_len]

    # ------------------------------------------------------------------
    # Sending packets
    # ------------------------------------------------------------------

    def send(self, packet: ESP3Packet):
        header = bytes(
            [
                (packet.data_length >> 8) & 0xFF,
                packet.data_length & 0xFF,
                packet.optional_length,
                packet.packet_type,
            ]
        )

        frame = bytearray()
        frame.append(SYNC_BYTE)
        frame.extend(header)
        frame.append(crc8(header))
        frame.extend(packet.data)
        frame.extend(packet.optional)
        frame.append(crc8(packet.data + packet.optional))

        self.transport.write(frame)
