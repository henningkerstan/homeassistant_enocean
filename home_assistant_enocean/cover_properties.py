from enum import IntFlag

from home_assistant_enocean.entity_properties import EnOceanEntityProperties


class EnOceanCoverProperties(EnOceanEntityProperties):
    def __init__(self, uid: str) -> None:

        """Construct EnOcean cover properties."""
        super().__init__()
        self.device_class = "cover"
        self.supported_features = IntFlag(0)  # Bitmask of supported features