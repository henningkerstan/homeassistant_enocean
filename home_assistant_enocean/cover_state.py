class EnOceanCoverState:
    def __init__(self) -> None:
        """Construct an EnOcean cover state."""
        self.position: int | None = None
        self.is_closed: bool | None = None
        self.is_closing: bool | None = None
        self.is_opening: bool | None = None
        self.position: int | None = None
