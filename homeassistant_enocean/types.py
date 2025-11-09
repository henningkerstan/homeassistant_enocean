from typing import Callable


type EnOceanEntityUID = str | None
"""An entity name which can be a string or None"""

type EnOceanDeviceIDString = str
"""An EnOcean device ID as string"""


type EnOceanCoverCallback = Callable[[int, int], None]
"""Callback type for cover state changes, with new position and tilt values."""

type EnOceanBinarySensorCallback = Callable[[bool], None]
"""Callback type for binary sensor state changes, with a boolean parameter indicating the new is_on state."""

type EnOceanLightCallback = Callable[[int, int], None]
"""Callback type for light state changes, with brightness and color temperature level as parameters."""

type EnOceanSwitchCallback = Callable[[bool], None]
"""Callback type for switch state changes, with a boolean parameter indicating the new is_on state."""