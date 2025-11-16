"""Representation of an EnOcean device state."""
import datetime
from ..entity_properties import HomeAssistantEntityProperties
from ..device_state import EnOceanDeviceState
from ..types import EnOceanBinarySensorCallback, EnOceanCoverCallback, EnOceanEntityUID, EnOceanLightCallback, EnOceanSendRadioPacket, EnOceanSensorCallback, EnOceanSwitchCallback
from ..device_type import EnOceanDeviceType
from ..address import EnOceanAddress, EnOceanDeviceAddress
from abc import abstractmethod, ABC
from enocean.protocol.packet import RadioPacket


class EnOceanDevice(ABC):
    """Representation of an EnOcean device."""

    def __init__(self, enocean_id: EnOceanDeviceAddress, device_type: EnOceanDeviceType, send_packet: EnOceanSendRadioPacket | None = None, device_name: str | None = None, sender_id: EnOceanAddress | None = None) -> None:
        """Construct an EnOcean device."""
        self.state: EnOceanDeviceState = EnOceanDeviceState()
        self.__enocean_id = enocean_id
        self.__device_type = device_type
        self.device_name = device_name
        self.__sender_id = sender_id

        self.__send_packet = send_packet
        self.__telegrams_received = 0

        # callbacks
        self._binary_sensor_callbacks: dict[EnOceanEntityUID, EnOceanBinarySensorCallback] = {}
        self._cover_callbacks: dict[EnOceanEntityUID, EnOceanCoverCallback] = {}
        self._light_callbacks: dict[EnOceanEntityUID, EnOceanLightCallback] = {}
        self._sensor_callbacks: dict[EnOceanEntityUID, EnOceanSensorCallback] = {}
        self._switch_callbacks: dict[EnOceanEntityUID, EnOceanSwitchCallback] = {}

        # entities
        self._binary_sensor_entities: list[HomeAssistantEntityProperties] = []
        self._cover_entities: list[HomeAssistantEntityProperties] = []
        self._light_entities: list[HomeAssistantEntityProperties] = []
        self.__internal_sensor_entities: list[HomeAssistantEntityProperties] = [
            HomeAssistantEntityProperties(unique_id="rssi", native_unit_of_measurement="dBm", device_class="signal_strength", entity_category="diagnostic"),
            HomeAssistantEntityProperties(unique_id="telegrams_received", sensor_state_class="total_increasing", entity_category="diagnostic", last_reset=datetime.datetime.now().astimezone()),
            HomeAssistantEntityProperties(unique_id="last_seen", device_class="timestamp", entity_category="diagnostic"),
        ]
        self._sensor_entitites: list[HomeAssistantEntityProperties] = []
        self._switch_entities: list[HomeAssistantEntityProperties] = []
        self.initialize_entities()


    @property
    def enocean_id(self) -> EnOceanDeviceAddress:
        """Return the device ID."""
        return self.__enocean_id

    @property
    def device_type(self) -> EnOceanDeviceType:
        """Return the device type."""
        return self.__device_type

    @property
    def sender_id(self) -> EnOceanAddress | None:
        """Return the sender ID."""
        return self.__sender_id
    
    @sender_id.setter
    def sender_id(self, value: EnOceanAddress | None) -> None:
        """Set the sender ID."""
        self.__sender_id = value

    @property
    def binary_sensor_entities(self) -> list[HomeAssistantEntityProperties]:
        """Return the binary sensor entities."""
        return self._binary_sensor_entities

    @property
    def cover_entities(self) -> list[HomeAssistantEntityProperties]:
        """Return the cover entities."""
        return self._cover_entities    
    
    @property
    def event_entities(self) -> list[HomeAssistantEntityProperties]:
        """Return the event entities."""
        return []

    @property
    def light_entities(self) -> list[HomeAssistantEntityProperties]:
        """Return the light entities."""
        return self._light_entities
    
    @property
    def sensor_entities(self) -> list[HomeAssistantEntityProperties]:
        """Return the sensor entities."""
        return self.__internal_sensor_entities + self._sensor_entitites

    @property
    def switch_entities(self) -> list[HomeAssistantEntityProperties]:
        """Return the switch entities."""
        return self._switch_entities

    
    def handle_packet(self, packet: RadioPacket, enocean_id: EnOceanDeviceAddress, sender_id: EnOceanAddress) -> None:
        """Handle an incoming EnOcean packet."""
        #print(f"EEPHandler.handle_packet: Checking packet from sender {EnOceanAddress.from_number(packet.sender_int)} against device ID {enocean_id.to_string()}")
        if packet.sender_int == enocean_id.to_number():
            rssi_callback = self._sensor_callbacks.get("rssi")
            if rssi_callback:
                rssi_callback(packet.dBm)
          
            self.__telegrams_received += 1
            telegram_seen_callback = self._sensor_callbacks.get("telegrams_received")
            if telegram_seen_callback:
                telegram_seen_callback(self.__telegrams_received)

            last_seen_callback = self._sensor_callbacks.get("last_seen")
            if last_seen_callback:
                last_seen_callback(datetime.datetime.now().astimezone())

            self.handle_matching_packet(packet, enocean_id, sender_id)

    def send_packet(self, packet: RadioPacket) -> None:
        """Send an EnOcean packet."""
        if self.__send_packet:
            self.__send_packet(packet)

    @abstractmethod
    def initialize_entities(self) -> None:
        """Initialize the entities handled by this EEP handler."""
        pass

    @abstractmethod
    def handle_matching_packet(self, packet: RadioPacket, enocean_id: EnOceanDeviceAddress, sender_id: EnOceanAddress) -> None:
        """Handle an incoming EnOcean packet."""
        pass
