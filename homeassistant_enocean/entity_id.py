from homeassistant_enocean.address import EnOceanDeviceAddress

class EnOceanEntityID:
    """An EnOcean entity is uniquely identified by its device's ID and a unique ID."""

    def __init__(self, device_address: EnOceanDeviceAddress, unique_id: str) -> None:
        """Construct an EnOcean entity ID."""
        self.__device_address = device_address
        self.__unique_id = unique_id

    @property 
    def device_address(self) -> EnOceanDeviceAddress:
        """Return the device address part of the entity ID."""
        return self.__device_address
    
    @property
    def unique_id(self) -> str:
        """Return the unique ID part of the entity ID."""
        return self.__unique_id

    def to_string(self) -> str:
        """Return a string representation of the entity."""
        return f"{self.__device_address.to_string()}.{self.__unique_id}"  if self.__unique_id else f"{self.__device_address.to_string()}"

    def __str__(self) -> str:
        """Return a string representation of the entity."""
        return self.to_string()

    def __hash__(self) -> int:
        """Return the hash of the entity ID."""
        return hash((self.__device_address.to_number(), self.unique_id))

    def __eq__(self, other) -> bool:
        """Check equality with another entity ID."""
        return (self.__device_address.to_number(), self.unique_id) == (other.device_address.to_number(), other.unique_id)
