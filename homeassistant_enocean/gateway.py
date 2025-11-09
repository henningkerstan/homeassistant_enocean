"""Representation of an EnOcean gateway."""
import logging
from typing import Callable, TypedDict

from enocean.communicators import SerialCommunicator
from enocean.protocol.packet import Packet, RadioPacket
from enocean.utils import to_hex_string
from homeassistant_enocean.entity_properties import HomeAssistantEntityProperties
from homeassistant_enocean.device_type import EnOceanDeviceType
from homeassistant_enocean.eep import EEP
from homeassistant_enocean.eep_handlers.eep_d2_05_00_handler import EEP_D2_05_00_Handler
from homeassistant_enocean.eep_handlers.eep_f6_02_handler import EEP_F6_02_Handler
from homeassistant_enocean.eep_handlers.eep_handler import EEPHandler
from homeassistant_enocean.entity_id import EnOceanEntityID
from homeassistant_enocean.types import EnOceanBinarySensorCallback, EnOceanCoverCallback, EnOceanDeviceIDString, EnOceanEventCallback, EnOceanLightCallback, EnOceanSwitchCallback
from .device import EnOceanDevice
from .address import EnOceanAddress

_LOGGER = logging.getLogger(__name__)

class ValueLabelDict(TypedDict):
    """Representation of a value/label dictionary."""

    def __init__(self, value: str, label: str) -> None:
        """Construct a value/label dictionary."""
        self.value = value
        self.label = label



class EnOceanHomeAssistantGateway:
    """Representation of an EnOcean gateway for Home Assistant."""

    def __init__(self, serial_path: str) -> None:
        """Initialize the EnOcean gateway."""
        self.__communicator: SerialCommunicator = SerialCommunicator(port=serial_path)
        self.__base_id: EnOceanAddress = EnOceanAddress(0)
        self.__chip_id: EnOceanAddress = EnOceanAddress(0)
        self.__chip_version: int = 0
        self.__sw_version: str = "n/a"
        self.__devices: dict[EnOceanDeviceIDString, EnOceanDevice] = {}
        self.__entity_update_callbacks: dict[str, Callable[[None], None]] = {}

        self.__binary_sensor_callbacks: dict[str, Callable[[bool], None]] = {}

        self.__eep_handlers: dict[EEP, EEPHandler] = {
            EEP(0xF6, 0x02, 0x01): EEP_F6_02_Handler(),
            EEP(0xF6, 0x02, 0x02): EEP_F6_02_Handler(),
            EEP(0xD2, 0x05, 0x00): EEP_D2_05_00_Handler(self.__communicator.send),
        }

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


        for device in self.__devices.values():
            # set device's sender id to base id if not set
            if not device.sender_id:
                device.sender_id = self.__base_id


    def stop(self) -> None:
        """Stop the EnOcean gateway."""
        if self.__communicator:
            if self.__communicator.is_alive():
                self.__communicator.stop()


    def add_device(self, enocean_id: EnOceanAddress, device_type: EnOceanDeviceType, device_name: str | None = None, sender_id: EnOceanAddress | None = None) -> None:
        """Add a device to the gateway."""
        if enocean_id.to_string() not in self.__devices:
            eep_handler = self.__eep_handlers.get(device_type.eep)
            if not eep_handler:
                print(f"No EEP handler for EEP {device_type.eep} found, cannot add device \"{device_name}\" ({enocean_id.to_string()}).")
                return           
            
            self.__devices[enocean_id.to_string()] = EnOceanDevice(
                enocean_id=enocean_id,
                device_type=device_type,
                handler=eep_handler,
                device_name=device_name,
                sender_id=sender_id,
            )
            print(f"Added device \"{device_name}\" ({enocean_id.to_string()} ({device_type.manufacturer} {device_type.model} EEP {device_type.eep}), sender ID: {sender_id.to_string() if sender_id else 'n/a'}) to gateway.")
            
            for d in self.__devices.values():
                print(f" - Device: \"{d.device_name}\" ({d.enocean_id.to_string()})")


    def register_binary_sensor_callback(self, entity_id: EnOceanEntityID, callback: EnOceanBinarySensorCallback) -> None:
        """Register a callback for a binary sensor entity."""
        print(f"Registering binary sensor callback for entity {entity_id.to_string()}")
        self.__devices[entity_id.device_address.to_string()].handler._binary_sensor_callbacks[entity_id.unique_id] = callback

    def register_cover_callback(self, entity_id: EnOceanEntityID, callback: EnOceanCoverCallback) -> None:
        """Register a callback for a cover entity."""
        print(f"Registering cover callback for entity {entity_id.to_string()}")
        self.__devices[entity_id.device_address.to_string()].handler._cover_callbacks[entity_id] = callback 


    def register_event_callback(self, event_type: str, callback: EnOceanEventCallback) -> None:
        """Register a callback for an event."""
        print(f"Registering event callback for event type {event_type}")
        self.__event_callbacks[event_type] = callback

    def register_switch_callback(self, entity_id: EnOceanEntityID, callback: EnOceanSwitchCallback) -> None:
        """Register a callback for a switch entity."""
        print(f"Registering switch callback for entity {entity_id.to_string()}")
        self.__switch_callbacks[entity_id.to_string()] = callback

    def register_light_callback(self, entity_id: EnOceanEntityID, callback: EnOceanLightCallback) -> None:
        """Register a callback for a light entity."""
        print(f"Registering light callback for entity {entity_id.to_string()}")
        self.__light_callbacks[entity_id.to_string()] = callback


    

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
    

    def get_device_properties(self, enocean_id: EnOceanAddress) -> EnOceanDevice | None:
        """Return the device properties for a given EnOcean ID."""
        return self.__devices.get(enocean_id.to_string())

    def _send_message_callback(self, command: Packet) -> None:
        """Send a command through the EnOcean gateway."""
        self.__communicator.send(command)

    def __handle_packet(self, packet: Packet) -> None:
        """Handle incoming EnOcean packet."""
        if not isinstance(packet, RadioPacket):
            return

        # find the device corresponding to the sender address
        device = self.__devices.get(EnOceanAddress(packet.sender_hex).to_string())
        if not device:
            print(f"Ignoring received packet from unknown device {EnOceanAddress(packet.sender_hex).to_string()}.")
            return
        
        print(f"Received packet from '{device.device_name}' ({packet.sender_hex}) with EEP {device.device_type.eep.to_string()}")

        # pass the packet to the device's EEP handler
        handler = device.handler
        if not handler:
            return
        
        print(f"Using EEP handler {handler.__class__.__name__} for device {device.device_name} ({device.enocean_id.to_string()}) to handle received packet.")
        handler.handle_packet(packet, device.enocean_id, device.sender_id)
        


    # Entity listings

    @property
    def binary_sensor_entities(self) -> dict[EnOceanEntityID, HomeAssistantEntityProperties]:
        """Return the list of binary sensor entities."""
        entities = {}

        # iterate over all devices and get their binary sensor entities
        for device in self.__devices.values():
            for entity in device.binary_sensor_entities:
                entity_id = EnOceanEntityID(
                    device_address=device.enocean_id,
                    unique_id=entity.unique_id,
                )
                entities[entity_id] = entity

        print(f"Binary sensor entities: {[str(e) for e in entities.keys()]}")
        return entities

    @property
    def cover_entities(self) -> dict[EnOceanEntityID, HomeAssistantEntityProperties]:
        """Return the list of cover entities."""
        entities = {}

        # iterate over all devices and get their cover entities
        for device in self.__devices.values():
            for entity in device.cover_entities:
                entity_id = EnOceanEntityID(
                    device_address=device.enocean_id,
                    unique_id=entity.unique_id,
                )
                entities[entity_id] = entity

        return entities
    
    @property
    def switch_entities(self) -> dict[EnOceanEntityID, HomeAssistantEntityProperties]:
        """Return the list of switch entities."""
        entities = {}

        # iterate over all devices and get their switch entities
        for device in self.__devices.values():
            for entity in device.switch_entities:
                entity_id = EnOceanEntityID(
                    device_address=device.enocean_id,
                    unique_id=entity.unique_id,
                )
                entities[entity_id] = entity

        return entities
    
    @property
    def light_entities(self) -> dict[EnOceanEntityID, HomeAssistantEntityProperties]:
        """Return the list of light entities."""
        entities = {}

        # iterate over all devices and get their light entities
        for device in self.__devices.values():
            for entity in device.light_entities:
                entity_id = EnOceanEntityID(
                    device_address=device.enocean_id,
                    unique_id=entity.unique_id,
                )
                entities[entity_id] = entity

        return entities

    
    def set_cover_position(self, enocean_entity_id: EnOceanEntityID, position: int) -> None:
        """Set the position of a cover device (0 = closed, 100 = open)."""
        pass

    def query_cover_position(self, enocean_entity_id: EnOceanEntityID) -> None:
        """Query the position of a cover device."""
        pass

    def stop_cover(self, enocean_entity_id: EnOceanEntityID) -> None:
        """Stop a cover device."""
        pass


    # methods for sending commands to devices
    # note that no such methods exist for sensors, as they do not accept commands

    # Light entities   
    def light_turn_on(self, enocean_entity_id: EnOceanEntityID, brightness: int | None = None, color_temp_kelvin: int | None = None) -> None:
        """Turn on a light device."""
        pass

    def light_turn_off(self, enocean_entity_id: EnOceanEntityID) -> None:
        """Turn off a light device."""
        pass


    # Switch entities
    def switch_turn_on(self, enocean_entity_id: EnOceanEntityID) -> None:
        """Turn on a switch device."""
        pass

    def switch_turn_off(self, enocean_entity_id: EnOceanEntityID) -> None:
        """Turn off a switch device."""
        pass