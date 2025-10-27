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
        return f"EnOceanEntity(enocean_id={self.enocean_id}, name={self.name}, device_class={self.device_class})"
    

    def __hash__(self):
        return hash((self.enocean_id, self.name, self.device_class))
    
    def __eq__(self, other):
        return (self.enocean_id, self.name, self.device_class) == (other.enocean_id, other.name, other.device_class)