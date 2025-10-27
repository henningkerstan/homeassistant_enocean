from asyncio import sleep
from home_assistant_enocean.gateway import EnOceanHomeAssistantGateway

from  home_assistant_enocean.device_type import EnOceanDeviceType
from devices import devices
from home_assistant_enocean.address import EnOceanAddress



async def main_loop():
    gateway = EnOceanHomeAssistantGateway(
        serial_path="/dev/tty.usbserial-EO8FD3C6",
    )

    await gateway.start()

    print("EnOcean Gateway started. Listening for packets...")


    for device in devices:
        device_type = EnOceanDeviceType.get_supported_device_types()[device["device_type"]]

        if not device_type:
            print(f"Device type {device['device_type']} not supported.")
            continue

        gateway.add_device(enocean_id=EnOceanAddress(device["enocean_id"]), device_type=device_type)

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