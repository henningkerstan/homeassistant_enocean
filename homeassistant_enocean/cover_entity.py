from homeassistant_enocean.entity_id import EnOceanEntityID


class EnOceanCoverEntity:
    """Representation of an EnOcean Cover Entity."""
    
    def __init__(self, entity_id: EnOceanEntityID) -> None:
        """Construct an EnOcean cover entity."""
        self.entity_id = entity_id


    