# ask for base id

import asyncio

from ..core.protocol import EnOceanProtocol


async def main():
    protocol = await EnOceanProtocol.open_serial_port("/dev/tty.usbserial-EO8FD3C6")
    protocol.add_packet_callback(lambda pkt: print(f"Received ESP3 packet: {pkt}"))
    protocol.add_erp1_callback(lambda erp1: print(f"Received ERP1 telegram: {erp1}"))

    # Keep the event loop running
    try:
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        print("\nShutting down...")


if __name__ == "__main__":
    asyncio.run(main())
