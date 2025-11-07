class EnOceanLightState:
    is_on: bool | None = None
    brightness: int | None = None  # 1..255
    color_temp_kelvin: int | None = None  # in Kelvin
