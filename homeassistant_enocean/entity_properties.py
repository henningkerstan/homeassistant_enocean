class HomeAssistantEntityProperties:
    """A collection of properties for a Home Assistant entity."""
    def __init__(self, unique_id: str | None = None, device_class: str | None = None, supported_features: int | None = None, translation_key: str | None = None) -> None:
        self.unique_id: str | None = unique_id
        self.device_class: str | None = device_class
        self.supported_features: int | None = supported_features  # Bitmask of supported features
        self.translation_key: str | None = translation_key


    def __str__(self):
        return (f"HomeAssistantEntityProperties("
                f"unique_id={self.unique_id}, "
                f"device_class={self.device_class}, "
                f"supported_features={self.supported_features}, "
                f"translation_key={self.translation_key})")
