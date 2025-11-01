class EnOceanCoverState:
    def __init__(self) -> None:
        """Construct an EnOcean cover state."""
        self.current_cover_position: int | None = None
        self.is_closed: bool | None = None
        self.is_closing: bool | None = None
        self.is_opening: bool | None = None

        self.stop_suspected: bool = False
        self.watchdog_enabled: bool = False
        self.watchdog_seconds_remaining: float = 0
        self.watchdog_queries_remaining: int = 5


    def __str__(self) -> str:
        """Return a string representation of the cover state."""
        return f"EnOceanCoverState(current_cover_position={self.current_cover_position}, is_closed={self.is_closed}, is_closing={self.is_closing}, is_opening={self.is_opening}, stop_suspected={self.stop_suspected}, watchdog_enabled={self.watchdog_enabled}, watchdog_seconds_remaining={self.watchdog_seconds_remaining}, watchdog_queries_remaining={self.watchdog_queries_remaining})"

