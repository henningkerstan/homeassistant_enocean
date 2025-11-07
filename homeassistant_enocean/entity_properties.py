from enum import IntFlag


class EnOceanEntityProperties:

    def __init__(self, uid: str | None = None, device_class: str | None = None, supported_features: IntFlag | None = None, translation_key: str | None = None) -> None:
        self.uid: str | None = uid
        self.device_class: str | None = None
        self.supported_features: IntFlag | None = None  # Bitmask of supported features
        self.translation_key: str | None = None