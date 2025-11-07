import asyncio
from enum import Enum, IntFlag
from home_assistant_enocean.address import EnOceanAddress
from home_assistant_enocean.cover_properties import EnOceanCoverProperties
from home_assistant_enocean.cover_state import EnOceanCoverState
from home_assistant_enocean.device_state import EnOceanDeviceState
from home_assistant_enocean.eep_handlers.eep_handler import EEPHandler
from home_assistant_enocean.entity_id import EnOceanEntityID
from enocean.protocol.packet import RadioPacket
from enocean.protocol.constants import RORG

WATCHDOG_TIMEOUT = 1
WATCHDOG_INTERVAL = 0.2
WATCHDOG_MAX_QUERIES = 10

class EnOceanCoverCommand(Enum):
    """The possible commands to be sent to an EnOcean cover."""

    SET_POSITION = 1
    STOP = 2
    QUERY_POSITION = 3


class EEP_D2_05_00_Handler(EEPHandler):
    """Handler for EnOcean Equipment Profile D2-05-00"""

    def cover_entities(self) -> list[EnOceanCoverProperties]:
        return [EnOceanCoverProperties(supported_features=IntFlag(1|2|4|8))]  # open, close, stop, set position
    

    def initialize_device(self, device_state: EnOceanDeviceState) -> None:
        """Initialize the device state."""
        print("Initializing EnOcean cover device with ID:", device_state.enocean_id.to_string())
        device_state.cover_state[None] = EnOceanCoverState()
        self.__send_cover_command(command=EnOceanCoverCommand.QUERY_POSITION, destination=device_state.enocean_id, sender=device_state.sender_id )


    def handle_packet_matching(self, packet: RadioPacket, device_state: EnOceanDeviceState) -> list[EnOceanEntityID]:
        """Handle an incoming EnOcean packet."""

        # position is inversed in Home Assistant and in EnOcean:
        # 0 means 'closed' in Home Assistant and 'open' in EnOcean
        # 100 means 'open' in Home Assistant and 'closed' in EnOcean
        new_position = 100 - packet.data[1]

        

        cover_state: EnOceanCoverState | None  = device_state.cover_state.get(None)
        if not cover_state:
            cover_state: EnOceanCoverState = EnOceanCoverState()
            device_state.cover_state[None] = cover_state

        print(f"Received EnOcean cover position: {new_position} for device {device_state.enocean_id.to_string()}; new state: {cover_state.__str__()}")

      
        # analyze position change and set opening/closing flags (might require watchdog)
        if cover_state.current_cover_position is not None:
            if new_position in (0, 100):
                cover_state.is_opening = False
                cover_state.is_closing = False
                self.stop_watchdog(cover_state)

            elif new_position == cover_state.current_cover_position:
                if cover_state.stop_suspected:
                    cover_state.stop_suspected = False
                    cover_state.is_opening = False
                    cover_state.is_closing = False
                    self.stop_watchdog(cover_state)
                else:
                    self.start_or_feed_watchdog(cover_state, device_state.enocean_id, device_state.sender_id)
                    cover_state.stop_suspected = True
                    return

            elif new_position > cover_state.current_cover_position:
                cover_state.is_opening = True
                cover_state.is_closing = False
                self.start_or_feed_watchdog(cover_state, device_state.enocean_id, device_state.sender_id)

            elif new_position < cover_state.current_cover_position:
                cover_state.is_opening = False
                cover_state.is_closing = True
                self.start_or_feed_watchdog(cover_state, device_state.enocean_id, device_state.sender_id)

        # assign new position
        cover_state.current_cover_position = new_position

        # set is_closed flag
        cover_state.is_closed = cover_state.current_cover_position == 0

        return [EnOceanEntityID(device_state.enocean_id, None)]



    def __send_cover_command(self, command: EnOceanCoverCommand, destination: EnOceanAddress, sender: EnOceanAddress, position: int = 0) -> None:
        """Send an EnOcean telegram with the respective command."""

        packet = RadioPacket.create(
            rorg=RORG.VLD,
            rorg_func=0x05,
            rorg_type=0x00,
            destination=destination.to_bytelist(),
            sender=sender.to_bytelist(),
            command=command.value,
            POS=position,
        )
        print(f"Sending EnOcean cover command {command.name} with position {position} ")
        self.send_packet(packet)

    def start_or_feed_watchdog(self, cover_state: EnOceanCoverState, destination: EnOceanAddress, sender: EnOceanAddress) -> None:
        """Start or feed the 'movement stop' watchdog."""

        print("Feeding 'movement stop' watchdog.")
        cover_state.watchdog_seconds_remaining = WATCHDOG_TIMEOUT
        cover_state.watchdog_queries_remaining = WATCHDOG_MAX_QUERIES

        if cover_state.watchdog_enabled:
            return

        print("Starting 'movement stop' watchdog.")
        cover_state.watchdog_enabled = True
        asyncio.create_task(self.watchdog(cover_state, destination, sender))


    def stop_watchdog(self, cover_state: EnOceanCoverState) -> None:
        """Stop the 'movement stop' watchdog."""
        print("Stopping 'movement stop' watchdog.")
        cover_state.watchdog_enabled = False
        

    async def watchdog(self, cover_state: EnOceanCoverState, destination: EnOceanAddress, sender: EnOceanAddress) -> None:
        """Watchdog to check if the cover movement stopped.

        After watchdog time expired, the watchdog queries the current status.
        """

        while 1:
            await asyncio.sleep(WATCHDOG_INTERVAL)

            if not cover_state.watchdog_enabled:
                return

            if cover_state.watchdog_seconds_remaining <= 0:
                self.send_telegram(EnOceanCoverCommand.QUERY_POSITION, destination, sender)
                cover_state.watchdog_seconds_remaining = WATCHDOG_TIMEOUT
                cover_state.watchdog_queries_remaining -= 1

                if cover_state.watchdog_queries_remaining == 0:
                    print(
                        "'Movement stop' watchdog max query limit reached. Disabling watchdog and setting state to 'unknown'"
                    )
                    cover_state.current_cover_position = None
                    cover_state.is_opening = False
                    cover_state.is_closing = False
                    return
                continue

            cover_state.watchdog_seconds_remaining -= WATCHDOG_INTERVAL