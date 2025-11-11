from typing import Callable


type EnOceanEntityUID = str | None
"""A string identifiying the entity uniquely within the context of an EnOcean device's platform.

Uniqueness is only per device and platform, thus, the same UID can be used for a binary sensor and a light entity of the same device.
"""

type EnOceanDeviceIDString = str
"""An EnOcean device ID as string"""

# Callbacks for state updates
type EnOceanBinarySensorCallback = Callable[[bool], None]
"""Callback type for binary sensor state changes, with a boolean parameter indicating the new is_on state."""

type EnOceanCoverCallback = Callable[[int], None]
"""Callback type for cover state changes, with new position (closed = 0, fully open = 100)."""

type EnOceanEventCallback = Callable[[str, dict], None]
"""Callback type for event notifications, with event type as string and additional data as dictionary."""

type EnOceanLightCallback = Callable[[bool, int, int], None]
"""Callback type for light state changes, with is_on state, brightness (1..255) and color temperature (in Kelvin) as parameters."""

type EnOceanSensorCallback = Callable[[int | float], None]
"""Callback type for binary sensor state changes, with a numeric parameter indicating the new state."""

type EnOceanSwitchCallback = Callable[[bool], None]
"""Callback type for switch state changes, with a boolean parameter indicating the new is_on state."""
