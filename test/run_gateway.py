from asyncio import sleep
from homeassistant_enocean.entity_id import EnOceanEntityID
from homeassistant_enocean.gateway import EnOceanHomeAssistantGateway

from  homeassistant_enocean.device_type import EnOceanDeviceType
from devices import devices
from homeassistant_enocean.address import EnOceanAddress

def binary_sensor_callback(entity_id: EnOceanEntityID, is_on: bool):
    print(f"Binary sensor {entity_id.to_string()} has state {'ON' if is_on else 'OFF'}")


def cover_callback(entity_id: EnOceanEntityID, position: int):
    print(f"Cover {entity_id.to_string()} has position {position}")

    
async def main_loop():
    print("Initializing EnOcean Gateway...")
    gateway = EnOceanHomeAssistantGateway(
        serial_path="/dev/tty.usbserial-EO8FD3C6",
    )


    for device in devices:
        device_type = EnOceanDeviceType.get_supported_device_types()[device["device_type"]]

        if not device_type:
            print(f"Device type {device['device_type']} not supported.")
            continue

        gateway.add_device(enocean_id=EnOceanAddress(device["enocean_id"]), device_type=device_type, device_name=device.get("name"), sender_id=EnOceanAddress(device["sender_id"]) if device.get("sender_id") else None  )

    
    for binary_sensor in gateway.binary_sensor_entities:
        print(f"Registered binary sensor entity: {binary_sensor.to_string()} with properties: {gateway.binary_sensor_entities[binary_sensor]}")
        gateway.register_binary_sensor_callback(binary_sensor, lambda is_on, entity_id=binary_sensor: binary_sensor_callback(entity_id, is_on))

    for cover in gateway.cover_entities:
        print(f"Registered cover entity: {cover.to_string()} with properties: {gateway.cover_entities[cover]}")
        gateway.register_cover_callback(cover, lambda position, entity_id=cover: cover_callback(entity_id, position))

    print("Starting EnOcean Gateway...")
    await gateway.start()
    print("EnOcean Gateway started. Listening for packets...")

    while True:
        try:
            await sleep(1)
        except KeyboardInterrupt:
            break
        except Exception:
            break

    if gateway.is_alive():
        gateway.stop()
    print("EnOcean Gateway stopped.")



if __name__ == "__main__":
    import asyncio

    asyncio.run(main_loop())