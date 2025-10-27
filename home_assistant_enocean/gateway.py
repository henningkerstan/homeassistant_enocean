"""Representation of an EnOcean gateway."""
import logging
from typing import Callable, TypedDict

from enocean.communicators import SerialCommunicator
from enocean.protocol.packet import Packet, RadioPacket
from enocean.utils import to_hex_string
from home_assistant_enocean.device_type import EnOceanDeviceType
from home_assistant_enocean.eep import EEP
from home_assistant_enocean.eep_f6_02_handler import EEP_F6_02_Handler
from home_assistant_enocean.eep_handler import EEPHandler
from home_assistant_enocean.entity_id import EnOceanEntityID
from home_assistant_enocean.types import EnOceanIDString, EntityName
from .cover_state import EnOceanCoverState
from .device_properties import EnOceanDeviceProperties
from .address import EnOceanAddress

_LOGGER = logging.getLogger(__name__)

class ValueLabelDict(TypedDict):
    """Representation of a value/label dictionary."""

    def __init__(self, value: str, label: str) -> None:
        """Construct a value/label dictionary."""
        self.value = value
        self.label = label


class EnOceanHomeAssistantGateway:
    """Representation of an EnOcean gateway for Home Assistant.
    """

    def __init__(self, serial_path: str) -> None:
        """Initialize the EnOcean gateway."""
        self.__communicator: SerialCommunicator = SerialCommunicator(port=serial_path)
        self.__base_id: EnOceanAddress = EnOceanAddress(0)
        self.__chip_id: EnOceanAddress = EnOceanAddress(0)
        self.__chip_version: int = 0
        self.__sw_version: str = "n/a"

        self.__devices: dict[EnOceanIDString, EnOceanDeviceProperties] = {}

        self.__eep_handlers: dict[EEP, EEPHandler] = {
            EEP(0xF6, 0x02, 0x01): EEP_F6_02_Handler(),
            EEP(0xF6, 0x02, 0x02): EEP_F6_02_Handler(),
        }

        # Map of entity UID to callback functions
        self.__entity_callbacks: dict[str, Callable[[None], None]] = {}

    async def start(self) -> None:
        """Start the EnOcean gateway."""
        self.__communicator.start()
        self.__chip_id = EnOceanAddress(to_hex_string(self.__communicator.chip_id))
        self.__base_id = EnOceanAddress(to_hex_string(self.__communicator.base_id))

        self.__chip_version = self.__communicator.version_info.chip_version

        self.__sw_version = (
            self.__communicator.version_info.app_version.versionString()
            + " (App), "
            + self.__communicator.version_info.api_version.versionString()
            + " (API)"
        )

        # callback needs to be set after initialization
        # in order for chip_id and base_id to be available
        self.__communicator.callback = self.__handle_packet


    def stop(self) -> None:
        """Stop the EnOcean gateway."""
        if self.__communicator:
            if self.__communicator.is_alive():
                self.__communicator.stop()

    def add_device(self, enocean_id: EnOceanAddress, device_type: EnOceanDeviceType) -> None:
        """Add a device to the gateway."""
        if enocean_id.to_string() not in self.__devices:
            self.__devices[enocean_id.to_string()] = EnOceanDeviceProperties(enocean_id, device_type)
            print(f"Added device {enocean_id.to_string()} ({device_type.manufacturer} {device_type.model} EEP {device_type.eep})")

    def register_entity_callback(self, entity_id: EnOceanEntityID, callback: Callable[[None], None]) -> None:
        """Register a callback for an entity."""
        print(f"Registering callback for entity {entity_id.to_string()}")
        self.__entity_callbacks[entity_id.to_string()] = callback

    @property
    def base_id(self) -> EnOceanAddress:
        """Returns the gateway's base id."""
        return self.__base_id

    @property
    def chip_id(self) -> EnOceanAddress:
        """Returns the gateway's chip id."""
        return self.__chip_id

    @property
    def valid_sender_ids(self) -> list[ValueLabelDict]:
        """Returns a list of valid sender ids."""

        if not self.__base_id or not self.__chip_id:
            return []

        valid_senders = [
            ValueLabelDict(
                value=self.__chip_id.to_string(),
                label="Chip ID (" + self.__chip_id.to_string() + ")",
            ),
            ValueLabelDict(
                value=self.__base_id.to_string(),
                label="Base ID (" + self.__base_id.to_string() + ")",
            ),
        ]
        base_id_int = self.__base_id.to_number()
        valid_senders.extend(
            [
                ValueLabelDict(
                    value=EnOceanAddress(base_id_int + i).to_string(),
                    label="Base ID + "
                    + str(i)
                    + " ("
                    + EnOceanAddress(base_id_int + i).to_string()
                    + ")",
                )
                for i in range(1, 128)
            ]
        )

        return valid_senders

    @property
    def chip_version(self) -> int:
        """Get the gateway's chip version."""
        return self.__chip_version

    @property
    def sw_version(self) -> str:
        """Get the gateway's software version."""
        return self.__sw_version
    

    def get_device_properties(self, enocean_id: EnOceanAddress) -> EnOceanDeviceProperties | None:
        """Return the device properties for a given EnOcean ID."""
        return self.__devices.get(enocean_id.to_string())

    def _send_message_callback(self, command: Packet) -> None:
        """Send a command through the EnOcean gateway."""
        self.__communicator.send(command)

    def __handle_packet(self, packet: Packet) -> None:
        """Handle incoming EnOcean packet."""
        if not isinstance(packet, RadioPacket):
            return

        try:
            rorg_hex = hex(packet.rorg)
        except TypeError:
            rorg_hex = None
        print(f"Received packet from {packet.sender_hex} with RORG {rorg_hex}")
     

        device_state = self.__devices.get(EnOceanAddress(packet.sender_hex).to_string())

        if not device_state:
            print(f"Unknown device {EnOceanAddress(packet.sender_hex).to_string()}, ignoring packet.")
            devices = self.__devices.keys()
            #print(f"Known devices: {[device.to_string() for device in devices]}")
            return
        


        eep = EEP.from_string(device_state.device_type.eep)

        handler = self.__eep_handlers.get(eep)
        if not handler:
            print(f"No handler for EEP {eep} found.")
            return
        

        print(f"Handling packet with EEP handler for {eep}.")
        updated_entities = handler.handle_packet(packet, device_state)
        for entity_id in updated_entities:
            print(f"Entity updated: {entity_id.to_string()}")
            callback = self.__entity_callbacks.get(entity_id.to_string())
            if callback:
                print(f"Invoking callback for entity {entity_id.to_string()}")
                callback()
            else:
                print(f"No callback registered for entity {entity_id.to_string()}")
            


    # Binary sensor entities
    @property
    def binary_sensor_entities(self) -> list[EnOceanEntityID]:
        """Return the list of binary sensor entities."""
        entities = []
        for enocean_id_string in self.__devices:
            device_state = self.__devices[enocean_id_string]
            eep = EEP.from_string(device_state.device_type.eep)
            handler = self.__eep_handlers.get(eep)
            if not handler:
                continue

            names = handler.binary_sensor_entities()
            for name in names:
                entities.append(EnOceanEntityID(device_state.enocean_id, name))
        return entities
                
    
    def binary_sensor_is_on(self, entity_id: EnOceanEntityID) -> bool | None:
        """Return whether a binary sensor device is on or off."""
        device_address_string = entity_id.device_address.to_string()
        if device_address_string in self.__devices:
            device_state = self.__devices[device_address_string]
            return device_state.binary_sensor_is_on.get(entity_id.name)
        

    # Cover entities
    def cover_current_cover_position(self, enocean_id: EnOceanAddress, name: str) -> int | None:
        """Return the current position of a cover device (0 = closed, 100 = open)."""
        if enocean_id.to_string() in self.__devices:
            device_state = self.__devices[enocean_id.to_string()]
            cover_state: EnOceanCoverState | None = device_state.cover_state.get(name)
            if cover_state:
                return cover_state.position

    def cover_is_closed(self, enocean_id: EnOceanAddress, name: str) -> bool | None:
        """Return whether a cover device is closed or not."""
        if enocean_id.to_string() in self.__devices:
            device_state = self.__devices[enocean_id.to_string()]
            cover_state: EnOceanCoverState | None = device_state.cover_state.get(name)
            if cover_state:
                return cover_state.is_closed
        return None

    def cover_is_closing(self, enocean_id: EnOceanAddress, name: str) -> bool | None:
        """Return whether a cover device is closing or not."""
        if enocean_id.to_string() in self.__devices:
            device_state = self.__devices[enocean_id.to_string()]
            cover_state: EnOceanCoverState | None = device_state.cover_state.get(name)
            if cover_state:
                return cover_state.is_closing
        return None

    def cover_is_opening(self, enocean_id: EnOceanAddress, name: str) -> bool | None:
        """Return whether a cover device is opening or not."""
        if enocean_id.to_string() in self.__devices:
            device_state = self.__devices[enocean_id.to_string()]
            cover_state: EnOceanCoverState | None = device_state.cover_state.get(name)
            if cover_state:
                return cover_state.is_opening
        return None
    
    def cover_open_cover(self, enocean_id: EnOceanAddress, name: str) -> None:
        """Open a cover device."""
        pass

    def cover_close_cover(self, enocean_id: EnOceanAddress, name: str) -> None:
        """Close a cover device."""
        pass

    def cover_set_cover_position(self, enocean_id: EnOceanAddress, name: str, position: int) -> None:
        """Set the position of a cover device (0 = closed, 100 = open)."""
        pass

    def cover_stop_cover(self, enocean_id: EnOceanAddress, name: str) -> None:
        """Stop a cover device."""
        pass


    # Light entities   
    def light_is_on(self, enocean_id: EnOceanAddress, name: str) -> bool | None:
        """Return whether a light device is on or off."""
        if enocean_id.to_string() in self.__devices:
            device_state = self.__devices[enocean_id.to_string()]
            light_state = device_state.light_state.get(name)
            if light_state:
                return light_state.is_on
        return None

    def light_brightness(self, enocean_id: EnOceanAddress, name: str) -> int | None:
        """Return the brightness of a light device between 1..255."""
        if enocean_id.to_string() in self.__devices:
            device_state = self.__devices[enocean_id.to_string()]
            light_state = device_state.light_state.get(name)
            if light_state:
                return light_state.brightness
        return None
    
    def light_color_temp_kelvin(self, enocean_id: EnOceanAddress, name: str) -> int | None:
        """Return the CT color value in K for a light device."""
        if enocean_id.to_string() in self.__devices:
            device_state = self.__devices[enocean_id.to_string()]
            light_state = device_state.light_state.get(name)
            if light_state:
                return light_state.color_temp_kelvin
        return None
    
    def light_turn_on(self, enocean_id: EnOceanAddress, name: str, brightness: int | None = None, color_temp_kelvin: int | None = None) -> None:
        """Turn on a light device."""
        pass

    def light_turn_off(self, enocean_id: EnOceanAddress, name: str) -> None:
        """Turn off a light device."""
        pass



    # Switch entities
    def switch_is_on(self, enocean_id: EnOceanAddress, name: str) -> bool | None:
        """Return whether a switch device is on or off."""
        if enocean_id.to_string() in self.__devices:
            device_state = self.__devices[enocean_id.to_string()]
            return device_state.switch_is_on.get(name)
        return None

    def switch_turn_on(self, enocean_id: EnOceanAddress, name: str) -> None:
        """Turn on a switch device."""
        pass