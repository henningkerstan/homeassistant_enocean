from home_assistant_enocean.address import EnOceanDeviceAddress

class EnOceanEntityID:
    """An EnOcean Entity is uniquely identified by its device's ID and a name."""

    def __init__(self, device_address: EnOceanDeviceAddress, name: str) -> None:
        """Construct an EnOcean entity ID."""
        self.__device_address = device_address
        self.__name = name

    @property 
    def device_address(self) -> EnOceanDeviceAddress:
        """Return the device address part of the entity ID."""
        return self.__device_address
    
    @property
    def name(self) -> str:
        """Return the name part of the entity ID."""
        return self.__name

    def to_string(self) -> str:
        """Return a string representation of the entity."""
        return f"{self.__device_address.to_string()}.{self.__name}"  if self.__name else f"{self.__device_address.to_string()}"

    def __str__(self) -> str:
        """Return a string representation of the entity."""
        return self.to_string()

    def __hash__(self) -> int:
        """Return the hash of the entity ID."""
        return hash((self.__device_address, self.__name))

    def __eq__(self, other) -> bool:
        """Check equality with another entity ID."""
        return (self.__device_address.to_number(), self.__name) == (other.device_address.to_number(), other.name)
