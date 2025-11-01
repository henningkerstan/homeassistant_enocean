"""Module containing a representation of a supported EnOcean device type."""

from home_assistant_enocean.eep import EEP


class EnOceanDeviceType:
    """Representation of a supported EnOcean device type."""

    __unique_id: str
    __eep: EEP
    __manufacturer: str
    __model: str

    def __init__(
        self,
        eep: EEP,
        unique_id: str | None = None,
        model: str = "",
        manufacturer: str = "Generic",
    ) -> None:
        """Construct an EnOcean device type."""
        
        if unique_id is None:
            unique_id = eep.to_string()
        self.__unique_id = unique_id
        self.__eep = eep
        self.__model = model
        self.__manufacturer = manufacturer

    @property
    def unique_id(self) -> str:
        """Return the unique id of this device type."""
        return self.__unique_id
    
    @property
    def eep(self) -> EEP:
        """Return the EEP of this device type."""
        return self.__eep
    
    @property
    def manufacturer(self) -> str:
        """Return the manufacturer of this device type."""
        return self.__manufacturer  
    
    @property
    def model(self) -> str:
        """Return the model of this device type."""
        return self.__model
    
    @property
    def is_generic_eep(self) -> bool:
        """Return true if this device type is a generic EEP."""
        return self.unique_id == self.eep.to_string()

    @property
    def label(self) -> str:
        """Return a label for this device type."""
        if self.is_generic_eep:
            return "EEP " + self.eep.to_string() + " (" + self.model + ")"
        return self.manufacturer + " " + self.model + " (EEP " + self.eep.to_string() + ")"

    @classmethod
    def get_supported_device_types(cls) -> dict[str, "EnOceanDeviceType"]:
        """Get a dictionary mapping from EnOcean device type id to EnOceanSupportedDeviceType."""
        return {
            # A5-02 Temperature Sensors
            "A5-02-01": EnOceanDeviceType(
                eep=EEP(0xA5, 0x02, 0x01),
                model="Temperature Sensor Range -40 °C to 0 °C",
            ),
            "A5-02-02": EnOceanDeviceType(
                eep=EEP(0xA5, 0x02, 0x02),
                model="Temperature Sensor Range -30 °C to +10 °C",
            ),
            "A5-02-03": EnOceanDeviceType(
                eep=EEP(0xA5, 0x02, 0x03),
                model="Temperature Sensor Range -20 °C to +20 °C",
            ),
            "A5-02-04": EnOceanDeviceType(
                eep=EEP(0xA5, 0x02, 0x04),
                model="Temperature Sensor Range -10 °C to +30 °C",
            ),
            "A5-02-05": EnOceanDeviceType(
                eep=EEP(0xA5, 0x02, 0x05),
                model="Temperature Sensor Range 0 °C to +40 °C",
            ),
            "A5-02-06": EnOceanDeviceType(
                eep=EEP(0xA5, 0x02, 0x06),
                model="Temperature Sensor Range +10 °C to +50 °C",
            ),
            "A5-02-07": EnOceanDeviceType(
                eep=EEP(0xA5, 0x02, 0x07),
                model="Temperature Sensor Range +20 °C to +60 °C",
            ),
            "A5-02-08": EnOceanDeviceType(
                eep=EEP(0xA5, 0x02, 0x08),
                model="Temperature Sensor Range +30 °C to +70 °C",
            ),
            "A5-02-09": EnOceanDeviceType(
                eep=EEP(0xA5, 0x02, 0x09),
                model="Temperature Sensor Range +40 °C to +80 °C",
            ),
            "A5-02-0A": EnOceanDeviceType(
                eep=EEP(0xA5, 0x02, 0x0A),
                model="Temperature Sensor Range +50 °C to +90 °C",
            ),
            "A5-02-0B": EnOceanDeviceType(
                eep=EEP(0xA5, 0x02, 0x0B),
                model="Temperature Sensor Range +60 °C to +100 °C",
            ),
            "A5-02-10": EnOceanDeviceType(
                eep=EEP(0xA5, 0x02, 0x10),
                model="Temperature Sensor Range -60 °C to +20 °C",
            ),
            "A5-02-11": EnOceanDeviceType(
                eep=EEP(0xA5, 0x02, 0x11),
                model="Temperature Sensor Range -50 °C to +30 °C",
            ),
            "A5-02-12": EnOceanDeviceType(
                eep=EEP(0xA5, 0x02, 0x12),
                model="Temperature Sensor Range -40 °C to +40 °C",
            ),
            "A5-02-13": EnOceanDeviceType(
                eep=EEP(0xA5, 0x02, 0x13),
                model="Temperature Sensor Range -30 °C to +50 °C",
            ),
            "A5-02-14": EnOceanDeviceType(
                eep=EEP(0xA5, 0x02, 0x14),
                model="Temperature Sensor Range -20 °C to +60 °C",
            ),
            "A5-02-15": EnOceanDeviceType(
                eep=EEP(0xA5, 0x02, 0x15),
                model="Temperature Sensor Range -10 °C to +70 °C",
            ),
            "A5-02-16": EnOceanDeviceType(
                eep=EEP(0xA5, 0x02, 0x16),
                model="Temperature Sensor Range 0 °C to +80 °C",
            ),
            "A5-02-17": EnOceanDeviceType(
                eep=EEP(0xA5, 0x02, 0x17),
                model="Temperature Sensor Range +10 °C to +90 °C",
            ),
            "A5-02-18": EnOceanDeviceType(
                eep=EEP(0xA5, 0x02, 0x18),
                model="Temperature Sensor Range +20 °C to +100 °C",
            ),
            "A5-02-19": EnOceanDeviceType(
                eep=EEP(0xA5, 0x02, 0x19),
                model="Temperature Sensor Range +30 °C to +110 °C",
            ),
            "A5-02-1A": EnOceanDeviceType(
                eep=EEP(0xA5, 0x02, 0x1A),
                model="Temperature Sensor Range +40 °C to +120 °C",
            ),
            "A5-02-1B": EnOceanDeviceType(
                eep=EEP(0xA5, 0x02, 0x1B),
                model="Temperature Sensor Range +50 °C to +130 °C",
            ),
            # A5-04 Temperature and Humidity sensors (only types 1 and 2)
            "A5-04-01": EnOceanDeviceType(
                eep=EEP(0xA5, 0x04, 0x01),
                model="Temperature and Humidity Sensor, Range 0 °C to +40 °C and 0% to 100%",
            ),
            "A5-04-02": EnOceanDeviceType(
                eep=EEP(0xA5, 0x04, 0x02),
                model="Temperature and Humidity Sensor, Range -20 °C to +60 °C and 0% to 100%",
            ),
            # A5-10 Room Operating Panels
            "A5-10-01": EnOceanDeviceType(
                eep=EEP(0xA5, 0x10, 0x01),
                model="Room Operating Panel Temperature Sensor, Set Point, Fan Speed and Occupancy Control",
            ),
            "A5-10-02": EnOceanDeviceType(
                eep=EEP(0xA5, 0x10, 0x02),
                model="Room Operating Panel Temperature Sensor, Set Point Control",
            ),
            "A5-10-03": EnOceanDeviceType(
                eep=EEP(0xA5, 0x10, 0x03),
                model="Room Operating Panel Temperature Sensor, Set Point Control",
            ),
            "A5-10-04": EnOceanDeviceType(
                eep=EEP(0xA5, 0x10, 0x04),
                model="Room Operating Panel Temperature Sensor, Set Point and Fan Speed Control",
            ),
            "A5-10-05": EnOceanDeviceType(
                eep=EEP(0xA5, 0x10, 0x05),
                model="Room Operating Panel Temperature Sensor, Set Point and Occupancy Control",
            ),
            "A5-10-06": EnOceanDeviceType(
                eep=EEP(0xA5, 0x10, 0x06),
                model="Room Operating Panel Temperature Sensor, Set Point and Day/Night Control",
            ),
            "A5-10-07": EnOceanDeviceType(
                eep=EEP(0xA5, 0x10, 0x07),
                model="Room Operating Panel Temperature Sensor, Fan Speed Control",
            ),
            "A5-10-08": EnOceanDeviceType(
                eep=EEP(0xA5, 0x10, 0x08),
                model="Room Operating Panel Temperature Sensor, Fan Speed and Occupancy Control",
            ),
            "A5-10-09": EnOceanDeviceType(
                eep=EEP(0xA5, 0x10, 0x09),
                model="Room Operating Panel Temperature Sensor, Fan Speed and Day/Night Control",
            ),
            "A5-10-0A": EnOceanDeviceType(
                eep=EEP(0xA5, 0x10, 0x0A),
                model="Room Operating Panel Temperature Sensor, Set Point Adjust and Single Input Contact",
            ),
            "A5-10-0B": EnOceanDeviceType(
                eep=EEP(0xA5, 0x10, 0x0B),
                model="Room Operating Panel Temperature Sensor and Single Input Contact",
            ),
            "A5-10-0C": EnOceanDeviceType(
                eep=EEP(0xA5, 0x10, 0x0C),
                model="Room Operating Panel Temperature Sensor and Occupancy Control",
            ),
            "A5-10-0D": EnOceanDeviceType(
                eep=EEP(0xA5, 0x10, 0x0D),
                model="Room Operating Panel Temperature Sensor and Day/Night Control",
            ),
            "A5-10-10": EnOceanDeviceType(
                eep=EEP(0xA5, 0x10, 0x10),
                model="Room Operating Panel Temperature and Humidity Sensor, Set Point and Occupancy Control",
            ),
            "A5-10-11": EnOceanDeviceType(
                eep=EEP(0xA5, 0x10, 0x11),
                model="Room Operating Panel Temperature and Humidity Sensor, Set Point and Day/Night Control",
            ),
            "A5-10-12": EnOceanDeviceType(
                eep=EEP(0xA5, 0x10, 0x12),
                model="Room Operating Panel Temperature and Humidity Sensor and Set Point",
            ),
            "A5-10-13": EnOceanDeviceType(
                eep=EEP(0xA5, 0x10, 0x13),
                model="Room Operating Panel Temperature and Humidity Sensor, Occupancy Control",
            ),
            "A5-10-14": EnOceanDeviceType(
                eep=EEP(0xA5, 0x10, 0x14),
                model="Room Operating Panel Temperature and Humidity Sensor, Day/Night Control",
            ),
            # A5-12 Automated Meter Reading
            "A5-12-01": EnOceanDeviceType(
                eep=EEP(0xA5, 0x12, 0x01),
                model="Automated Meter Reading AMR - Electricity",
            ),
            # A5-20 HVAC Components - Battery Powered Actuator (BI-DIR)
            "A5-20-01": EnOceanDeviceType(
                eep=EEP(0xA5, 0x20, 0x01),
                model="HVAC Components - Battery Powered Actuator BI-DIR",
            ),
            # D2-01 Electronic Switches and Dimmers with Energy Measurement and Local Control
            "D2-01-00": EnOceanDeviceType(
                eep=EEP(0xD2, 0x01, 0x00),
                model="Electronic Switches and Dimmers with Energy Measurement and Local Control, Type 00",
            ),
            "D2-01-01": EnOceanDeviceType(
                eep=EEP(0xD2, 0x01, 0x01),
                model="Electronic Switches and Dimmers with Energy Measurement and Local Control, Type 01",
            ),
            "D2-01-03": EnOceanDeviceType(
                eep=EEP(0xD2, 0x01, 0x03),
                model="Electronic Switches and Dimmers with Energy Measurement and Local Control, Type 03",
            ),
            "D2-01-04": EnOceanDeviceType(
                eep=EEP(0xD2, 0x01, 0x04),
                model="Electronic Switches and Dimmers with Energy Measurement and Local Control, Type 04",
            ),
            "D2-01-05": EnOceanDeviceType(
                eep=EEP(0xD2, 0x01, 0x05),
                model="Electronic Switches and Dimmers with Energy Measurement and Local Control, Type 05",
            ),
            "D2-01-06": EnOceanDeviceType(
                eep=EEP(0xD2, 0x01, 0x06),
                model="Electronic Switches and Dimmers with Energy Measurement and Local Control, Type 06",
            ),
            "D2-01-07": EnOceanDeviceType(
                eep=EEP(0xD2, 0x01, 0x07),
                model="Electronic Switches and Dimmers with Energy Measurement and Local Control, Type 07",
            ),
            "D2-01-08": EnOceanDeviceType(
                eep=EEP(0xD2, 0x01, 0x08),
                model="Electronic Switches and Dimmers with Energy Measurement and Local Control, Type 08",
            ),
            "D2-01-09": EnOceanDeviceType(
                eep=EEP(0xD2, 0x01, 0x09),
                model="Electronic Switches and Dimmers with Energy Measurement and Local Control, Type 09",
            ),
            "D2-01-0A": EnOceanDeviceType(
                eep=EEP(0xD2, 0x01, 0x0A),
                model="Electronic Switches and Dimmers with Energy Measurement and Local Control, Type 0A",
            ),
            "D2-01-0B": EnOceanDeviceType(
                eep=EEP(0xD2, 0x01, 0x0B),
                model="Electronic Switches and Dimmers with Energy Measurement and Local Control, Type 0B",
            ),
            "D2-01-0C": EnOceanDeviceType(
                eep=EEP(0xD2, 0x01, 0x0C),
                model="Electronic Switches and Dimmers with Energy Measurement and Local Control, Type 0C",
            ),
            "D2-01-0D": EnOceanDeviceType(
                eep=EEP(0xD2, 0x01, 0x0D),
                model="Electronic Switches and Dimmers with Energy Measurement and Local Control, Type 0D",
            ),
            "D2-01-0E": EnOceanDeviceType(
                eep=EEP(0xD2, 0x01, 0x0E),
                model="Electronic Switches and Dimmers with Energy Measurement and Local Control, Type 0E",
            ),
            "D2-01-0F": EnOceanDeviceType(
                eep=EEP(0xD2, 0x01, 0x0F),
                model="Electronic Switches and Dimmers with Energy Measurement and Local Control, Type 0F",
            ),
            "D2-01-10": EnOceanDeviceType(
                eep=EEP(0xD2, 0x01, 0x10),
                model="Electronic Switches and Dimmers with Energy Measurement and Local Control, Type 10",
            ),
            "D2-01-11": EnOceanDeviceType(
                eep=EEP(0xD2, 0x01, 0x11),
                model="Electronic Switches and Dimmers with Energy Measurement and Local Control, Type 11",
            ),
            "D2-01-12": EnOceanDeviceType(
                eep=EEP(0xD2, 0x01, 0x12),
                model="Electronic Switches and Dimmers with Energy Measurement and Local Control, Type 12",
            ),
            "D2-01-13": EnOceanDeviceType(
                eep=EEP(0xD2, 0x01, 0x13),
                model="Electronic Switches and Dimmers with Energy Measurement and Local Control, Type 13",
            ),
            "D2-01-14": EnOceanDeviceType(
                eep=EEP(0xD2, 0x01, 0x14),
                model="Electronic Switches and Dimmers with Energy Measurement and Local Control, Type 14",
            ),
            # D2-05-00 Blinds Control for Position and Angle
            "D2-05-00": EnOceanDeviceType(
                eep=EEP(0xD2, 0x05, 0x00),
                model="Blinds Control for Position and Angle, Type 00",
            ),
            # F6-02 Light and Blind Control
            "F6-02-01": EnOceanDeviceType(
                eep=EEP(0xF6, 0x02, 0x01),
                model="Light and Blind Control - Application Style 2",
            ),
            "F6-02-02": EnOceanDeviceType(
                eep=EEP(0xF6, 0x02, 0x02),
                model="Light and Blind Control - Application Style 1",
            ),
            # F6-10-00 Window Handle
            "F6-10-00": EnOceanDeviceType(
                eep=EEP(0xF6, 0x10, 0x00),
                model="Mechanical Handle - Window Handle",
            ),
            # Other Devices
            "Eltako_FUD61NPN": EnOceanDeviceType(
                unique_id="Eltako_FUD61NPN",
                eep=EEP(0xA5, 0x38, 0x08),
                manufacturer="Eltako",
                model="FUD61NPN-230V Wireless universal dimmer",
            ),
            "Eltako_FLD61": EnOceanDeviceType(
                unique_id="Eltako_FLD61",
                eep=EEP(0xA5, 0x38, 0x08),
                manufacturer="Eltako",
                model="FLD61 PWM LED dimmer switch for LEDs 12-36V DC, up to 4A",
            ),
            "Eltako_FT55": EnOceanDeviceType(
                unique_id="Eltako_FT55",
                eep=EEP(0xF6, 0x02, 0x01),
                manufacturer="Eltako",
                model="FT55 battery-less wall switch",
            ),
            "Jung_ENO": EnOceanDeviceType(
                unique_id="Jung_ENO",
                eep=EEP(0xF6, 0x02, 0x01),
                manufacturer="Jung",
                model="ENO Series",
            ),
            "Omnio_WS-CH-102": EnOceanDeviceType(
                unique_id="Omnio_WS-CH-102",
                eep=EEP(0xF6, 0x02, 0x01),
                manufacturer="Omnio",
                model="WS-CH-102",
            ),
            "Hoppe_SecuSignal": EnOceanDeviceType(
                unique_id="Hoppe_SecuSignal",
                eep=EEP(0xF6, 0x10, 0x00),
                manufacturer="Hoppe",
                model="SecuSignal window handle from Somfy",
            ),
            "TRIO2SYS_WallSwitches": EnOceanDeviceType(
                unique_id="TRIO2SYS_WallSwitches",
                eep=EEP(0xF6, 0x02, 0x01),
                manufacturer="TRIO2SYS",
                model="TRIO2SYS Wall switches",
            ),
            "NodOn_SIN-2-1-01": EnOceanDeviceType(
                unique_id="NodOn_SIN-2-1-01",
                eep=EEP(0xD2, 0x01, 0x0F),
                manufacturer="NodOn",
                model="SIN-2-1-01 Single Channel Relay Switch",
            ),
            "NodOn_SIN-2-2-01": EnOceanDeviceType(
                unique_id="NodOn_SIN-2-2-01",
                eep=EEP(0xD2, 0x01, 0x12),
                manufacturer="NodOn",
                model="SIN-2-2-01 Dual Channel Relay Switch",
            ),
            "NodOn_SIN-2-RS-01": EnOceanDeviceType(
                unique_id="NodOn_SIN-2-RS-01",
                eep=EEP(0xD2, 0x05, 0x00),
                manufacturer="NodOn",
                model="SIN-2-RS-01 Roller Shutter Controller",
            ),
            "Permundo_PSC234": EnOceanDeviceType(
                unique_id="Permundo_PSC234",
                eep=EEP(0xD2, 0x01, 0x09),
                manufacturer="Permundo",
                model="PSC234 (switch and power monitor)",
            ),
            "NodOn_PIR-2-1-01": EnOceanDeviceType(
                unique_id="NodOn_PIR-2-1-01",
                eep=EEP(0xA5, 0x07, 0x03),
                manufacturer="NodOn",
                model="PIR-2-1-01 Motion Sensor (NOT TESTED)",
            ),
        }
