class EEP:
    """Representation of an EnOcean Equipment Profile (EEP)."""

    def __init__(self, rorg: int, func: int, type_: int) -> None:
        """Construct an EnOcean Equipment Profile."""
        self.rorg = rorg
        self.func = func
        self.type = type_