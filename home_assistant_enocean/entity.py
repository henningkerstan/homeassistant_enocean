from home_assistant_enocean.entity_name import EntityName
from home_assistant_enocean.id import EnOceanID


class EnOceanEntity:
    """Representation of an EnOcean entity."""

    def __init__(self, enocean_id: EnOceanID, name: EntityName, device_class: str | None = None) -> None:
        """Construct an EnOcean entity."""
        self.name = name
        self.enocean_id = enocean_id
        self.device_class = device_class


    def __str__(self) -> str:
        """Return a string representation of the entity."""
        return f"EnOceanEntity(name={self.name}, enocean_id={self.enocean_id}, device_class={self.device_class})"