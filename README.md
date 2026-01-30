# homeassistant_enocean
This is a wrapper library to integrate the [EnOcean](https://www.enocean.com/) protocol into [Home Assistant](https://www.home-assistant.io).


## Usage
This library is specifically written for Home Assistant's [EnOcean integration](https://www.home-assistant.io/integrations/enocean/). You can therefore best see how to use it by viewing its [source code on GitHub](https://github.com/henningkerstan/home-assistant-core/tree/enocean-options-flow). The library follows these [rules](https://developers.home-assistant.io/docs/api_lib_index).

## Supported EnOcean devices based on their EnOcean Equipment Profiles (EEP)

| EEP | Description | Home Assistant Component(s) | Tested Device(s) |
|-----|-------------|----------|----------|
| A5-02-01 | Temperature Sensor Range -40 °C to +100 °C | one sensor | none (untested) |
| A5-02-02 | Temperature Sensor Range -40 °C to +100 °C | one sensor | none (untested) |
| A5-02-03 | Temperature Sensor Range -40 °C to +100 °C | one sensor | none (untested) |
| A5-02-04 | Temperature Sensor Range -40 °C to +100 °C | one sensor | none (untested) |
| A5-02-05 | Temperature Sensor Range -40 °C to +100 °C | one sensor | none (untested) |
| A5-02-06 | Temperature Sensor Range -40 °C to +100 °C | one sensor | none (untested) |
| A5-02-07 | Temperature Sensor Range -40 °C to +100 °C | one sensor | none (untested) |
| A5-02-08 | Temperature Sensor Range -40 °C to +100 °C | one sensor | none (untested) |
| A5-02-09 | Temperature Sensor Range -40 °C to +100 °C | one sensor | none (untested) |
| A5-02-0A | Temperature Sensor Range -40 °C to +100 °C | one sensor | none (untested) |
| A5-02-0B | Temperature Sensor Range -40 °C to +100 °C | one sensor | none (untested) |
| A5-02-10 | Temperature Sensor Range -60 °C to +130 °C | one sensor | none (untested) |
| A5-02-11 | Temperature Sensor Range -60 °C to +130 °C | one sensor | none (untested) |
| A5-02-12 | Temperature Sensor Range -60 °C to +130 °C | one sensor | none (untested) |
| A5-02-13 | Temperature Sensor Range -60 °C to +130 °C | one sensor | none (untested) |
| A5-02-14 | Temperature Sensor Range -60 °C to +130 °C | one sensor | none (untested) |
| A5-02-15 | Temperature Sensor Range -60 °C to +130 °C | one sensor | none (untested) |
| A5-02-16 | Temperature Sensor Range -60 °C to +130 °C | one sensor | none (untested) |
| A5-02-17 | Temperature Sensor Range -60 °C to +130 °C | one sensor | none (untested) |
| A5-02-18 | Temperature Sensor Range -60 °C to +130 °C | one sensor | none (untested) |
| A5-02-19 | Temperature Sensor Range -60 °C to +130 °C | one sensor | none (untested) |
| A5-02-1A | Temperature Sensor Range -60 °C to +130 °C | one sensor | none (untested) |
| A5-02-1B | Temperature Sensor Range -60 °C to +130 °C | one sensor | none (untested) |
| A5-02-20 | 10 Bit Temperature Sensor Range -10°C to +41.2°C | one sensor | none (untested) |
| A5-02-30 | 10 Bit Temperature Sensor Range -40°C to +62.3°C | one sensor | none (untested) |
| A5-04-01 | Temperature and Humidity Sensor, 0 °C to +40 °C, 0% to 100% | two sensors (`temperature`, `humidity`) | none (untested) |
| A5-04-02 | Temperature and Humidity Sensor, -20 °C to +60 °C, 0% to 100% | two sensors (`temperature`, `humidity`) | none (untested) |
| A5-04-03 | Temperature and Humidity Sensor, -20°C to +60°C 10bit, 0% to 100% | two sensors (`temperature`, `humidity`) | none (untested) |
| A5-04-04 | Temperature and Humidity Sensor, -40°C to +120°C 12bit, 0% to 100% | two sensors (`temperature`, `humidity`) | none (untested) |
| A5-06-01 | Light Sensor, Range 300lx to 60.000lx | one sensor (`illuminance`) and (if not Eltako), another sensor (`supply voltage`) | Eltako FAH65S (hence, only `illuminance` sensor is tested) |
| A5-07-03 | Occupancy with Supply voltage monitor and 10-bit illumination | one binary sensor (`motion_detected`) and two sensors (`illuminance`, `supply_voltage`) | NodOn PIR-2-1-01 |
| A5-08-01 | Light, temperature and occupancy sensor, 0lx to 510lx, 0°C to 51°C | one binary sensor (`occupancy`) and one sensor (`supply_voltage`); for non-Eltako devices an additional binary sensor (`occupancy_button`) and an additional sensor (`temperature`) | Eltako FABH65S |
| A5-38-08 | Gateway | one light, three diagnostic numbers (`ramping_time`, `min_brightness`, `max_brightness`) and two diagnostic sensors (`device_properties`, `dimming_range`) | Eltako FUD61NPN-230V |
| D2-01-00 | Electronic Switches and Dimmers with Energy Measurement | one switch | none (untested) |
| D2-01-01 | Electronic Switches and Dimmers with Energy Measurement | one switch | none (untested) |
| D2-01-02 | Electronic Switches and Dimmers with Energy Measurement | one switch | none (untested) |
| D2-01-03 | Electronic Switches and Dimmers with Energy Measurement | one switch | none (untested) |
| D2-01-04 | Electronic Switches and Dimmers with Energy Measurement | one switch | none (untested) |
| D2-01-05 | Electronic Switches and Dimmers with Energy Measurement | one switch | none (untested) |
| D2-01-06 | Electronic Switches and Dimmers with Energy Measurement | one switch | none (untested) |
| D2-01-07 | Electronic Switches and Dimmers with Energy Measurement | one switch | none (untested) |
| D2-01-08 | Electronic Switches and Dimmers with Energy Measurement | one switch | none (untested) |
| D2-01-09 | Electronic Switches and Dimmers with Energy Measurement | one switch | none (untested) |
| D2-01-0A | Electronic Switches and Dimmers with Energy Measurement | one switch | none (untested) |
| D2-01-0B | Electronic Switches and Dimmers with Energy Measurement | one switch | none (untested) |
| D2-01-0C | Electronic Switches and Dimmers with Energy Measurement | one switch | none (untested) |
| D2-01-0D | Electronic Switches and Dimmers with Energy Measurement | one switch | none (untested) |
| D2-01-0E | Electronic Switches and Dimmers with Energy Measurement | one switch | none (untested) |
| D2-01-0F | Electronic Switches and Dimmers with Energy Measurement | one switch | NodOn SIN-2-1-01 |
| D2-01-10 | Electronic Switches and Dimmers with Energy Measurement | two switches | none (untested) |
| D2-01-11 | Electronic Switches and Dimmers with Energy Measurement | two switches | none (untested) |
| D2-01-12 | Electronic Switches and Dimmers with Energy Measurement | two switches | none (untested) |
| D2-01-13 | Electronic Switches and Dimmers with Energy Measurement | four switches | none (untested) |
| D2-01-14 | Electronic Switches and Dimmers with Energy Measurement | eight switches | none (untested) |
| D2-05-00 | Blinds Control for Position and Angle | one cover | NodOn SIN-2-RS-01 |
| F6-02-01 | Light and Blind Control - Application Style 2 | eight binary sensors (`a0`, `a1`, `b0`, `b1`, `ab0`, `ab1`, `a0b1`, `a1b0`) | Jung ENO wall switch (2 channels) |
| F6-02-02 | Light and Blind Control - Application Style 1 | eight binary sensors (`a0`, `a1`, `b0`, `b1`, `ab0`, `ab1`, `a0b1`, `a1b0`) | Jung ENO wall switch (2 channels) |
| F6-10-00 | Mechanical Handle - Window Handle | one sensor (`up2vertical`, `vertical2up`, `down2vertical`, `vertical2down`) | none (untested) |

Each supported device has three additional diagnostic sensors:
 - `rssi`: the received signal strength (in dBm) of the last received telegram
 - `telegrams_received`: the number of telegrams received since last gateway start
 - `last_seen`: timestamp of the last received telegram





## Development
After cloning this repository, execute the provided [scripts/setup.sh](scripts/setup.sh) to set up the development environment.

## Dependencies
This library only has one dependency, namely

- [enocean4ha](https://github.com/topic2k/enocean4ha/tree) in version 0.71.0, which is MIT-licensed.

The reason for using this library instead of the previously used [enocean](https://github.com/kipe/enocean) library is a more extended set of supported EnOcean Equipment Profiles (EEP).

## Copyright & license
Copyright 2026 Henning Kerstan

Licensed under the Apache License, Version 2.0 (the "License"). See [LICENSE](./LICENSE) file for details.

