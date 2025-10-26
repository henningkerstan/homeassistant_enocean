class EEP:
    """Representation of an EnOcean Equipment Profile (EEP)."""

    def __init__(self, rorg: int, func: int, type_: int) -> None:
        """Construct an EnOcean Equipment Profile."""
        self.rorg = rorg
        self.func = func
        self.type = type_


    @classmethod
    def supported_eeps(cls) -> list["EEP"]:
        return {
            EEP(0xF6, 0x00, 0x01), 
        }
    
    @classmethod
    def from_string(cls, eep_string: str) -> "EEP":
        """Create an EEP instance from a dash-separated string."""  
        parts = eep_string.strip().split("-")
        if len(parts) != 3:
            raise ValueError("Wrong format.")
        rorg = int(parts[0], 16)
        func = int(parts[1], 16)
        type_ = int(parts[2], 16)
        return cls(rorg, func, type_)
    
    def __hash__(self):
        return hash((self.rorg, self.func, self.type))
    
    def __eq__(self, other):
        return (self.rorg, self.func, self.type) == (other.rorg, other.func, other.type)
    

    def __str__(self):
        return f"{self.rorg:02X}-{self.func:02X}-{self.type:02X}"