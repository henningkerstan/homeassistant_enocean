from home_assistant_enocean.entity_name import EntityName
from home_assistant_enocean.id import EnOceanID


class EnOceanEntity:
    """Representation of an EnOcean entity."""

    def __init__(self, enocean_id: EnOceanID, name: EntityName) -> None:
        """Construct an EnOcean entity."""
        self.name = name
        self.enocean_id = enocean_id
        