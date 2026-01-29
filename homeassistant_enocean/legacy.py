"""Legacy imports from the underlying 'enocean' library for backward compatibility.

This module re-exports selected classes and functions from the 'enocean' library
to maintain compatibility with existing code that relies on these imports.

It will be removed in future versions, as soon as the Home Assistant integration
code has been migrated to use the 'homeassistant_enocean' library instead.
"""

from enocean.utils import combine_hex
from enocean.communicators import SerialCommunicator
from enocean.protocol.packet import Packet, RadioPacket

# from .eep import EEP

__all__ = [
    "combine_hex",
    "SerialCommunicator",
    "Packet",
    "RadioPacket",
]


# def determine_eep(platform: str) -> EEP():
